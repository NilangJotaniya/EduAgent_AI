import os

PDF_STORAGE_DIR = "uploaded_pdfs"
VECTOR_DB_DIR = "vector_db"

os.makedirs(PDF_STORAGE_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)


class PDFProcessor:
    """
    Processes PDF documents and enables semantic (meaning-based) search.

    The embedding model used is "all-MiniLM-L6-v2":
    - Small and fast (runs on CPU)
    - Free and open-source
    - Downloads automatically on first use (~90MB)
    - Converts text to 384-dimensional vectors
    """

    def __init__(self):
        self.vectorstore = None
        self._try_load_existing_vectorstore()

    def _try_load_existing_vectorstore(self):
        """
        On startup, try to load a previously saved vector database.
        If PDFs were uploaded before, we can use them right away.
        """
        if not os.path.exists(VECTOR_DB_DIR):
            return
        if not os.listdir(VECTOR_DB_DIR):
            return

        try:
            from langchain_community.vectorstores import Chroma
            from langchain_community.embeddings import HuggingFaceEmbeddings

            print("📂 Loading existing PDF knowledge base from disk...")

            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )

            self.vectorstore = Chroma(
                persist_directory=VECTOR_DB_DIR,
                embedding_function=embeddings
            )
            print("✅ PDF knowledge base loaded successfully")

        except ImportError as e:
            print(f"⚠️  LangChain libraries not installed: {e}")
            print("   Run: pip install langchain langchain-community chromadb sentence-transformers pypdf")
        except Exception as e:
            print(f"⚠️  Could not load existing vector DB: {e}")

    def process_pdf(self, pdf_file_path: str, filename: str) -> dict:
        """
        Read a PDF, extract text, create embeddings, store in ChromaDB.

        Parameters:
            pdf_file_path (str): Full path to the saved PDF file
            filename      (str): Original filename for tracking

        Returns:
            dict: {
                "success": True/False,
                "pages": number of pages read,
                "chunks": number of text chunks created,
                "filename": filename,
                "error": error message (only if success=False)
            }
        """
        try:
            from langchain_community.document_loaders import PyPDFLoader
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            from langchain_community.vectorstores import Chroma
            from langchain_community.embeddings import HuggingFaceEmbeddings

            # ---- Step 1: Load PDF ----
            print(f"📖 Reading PDF: {filename}")
            loader = PyPDFLoader(pdf_file_path)
            pages = loader.load()

            if not pages:
                return {
                    "success": False,
                    "error": "PDF appears to be empty or could not be read."
                }

            print(f"   → Extracted text from {len(pages)} pages")

            # ---- Step 2: Split into Chunks ----
            # Why chunks? LLMs have token limits.
            # Instead of sending the whole 100-page document,
            # we find the 3 most relevant chunks and send only those.
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,       # Each chunk ~500 characters
                chunk_overlap=50,     # 50-char overlap prevents losing context at edges
                separators=["\n\n", "\n", ".", " ", ""]
            )
            chunks = text_splitter.split_documents(pages)

            if not chunks:
                return {
                    "success": False,
                    "error": "Could not extract readable text from this PDF."
                }

            # Tag each chunk with the source filename
            for chunk in chunks:
                chunk.metadata["source_file"] = filename

            print(f"   → Split into {len(chunks)} searchable chunks")

            # ---- Step 3: Create Embeddings ----
            # The embedding model converts text to numbers (vectors)
            # so we can do mathematical similarity comparison.
            print("   → Creating text embeddings (this may take a moment)...")
            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )

            # ---- Step 4: Store in ChromaDB ----
            if self.vectorstore is None:
                # First PDF — create a new vector database
                self.vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    persist_directory=VECTOR_DB_DIR
                )
            else:
                # Additional PDF — add to existing database
                self.vectorstore.add_documents(chunks)

            # Save to disk (persists between app restarts)
            self.vectorstore.persist()

            print(f"✅ PDF '{filename}' processed successfully!")
            return {
                "success": True,
                "pages": len(pages),
                "chunks": len(chunks),
                "filename": filename
            }

        except ImportError as e:
            msg = f"Missing library: {e}. Run: pip install langchain langchain-community chromadb sentence-transformers pypdf"
            print(f"❌ {msg}")
            return {"success": False, "error": msg}

        except Exception as e:
            print(f"❌ PDF processing error: {e}")
            return {"success": False, "error": str(e)}

    def search(self, query: str, num_results: int = 3) -> str:
        """
        Search the vector database for content relevant to the query.

        Uses cosine similarity — finds stored text chunks whose
        meaning (vector) is most similar to the query's meaning.

        Parameters:
            query       (str): The student's question
            num_results (int): How many chunks to return (default: 3)

        Returns:
            str: Most relevant text chunks combined, or "" if nothing found
        """
        if self.vectorstore is None:
            return ""  # No PDFs have been uploaded yet

        try:
            docs = self.vectorstore.similarity_search(query, k=num_results)

            if not docs:
                return ""

            # Combine results, showing which file each came from
            results = []
            for doc in docs:
                source = doc.metadata.get("source_file", "College Document")
                results.append(f"[Source: {source}]\n{doc.page_content}")

            return "\n\n".join(results)

        except Exception as e:
            print(f"⚠️  PDF search error: {e}")
            return ""

    def get_uploaded_files(self) -> list:
        """Return list of PDF files in the upload directory."""
        if not os.path.exists(PDF_STORAGE_DIR):
            return []
        return [f for f in os.listdir(PDF_STORAGE_DIR) if f.endswith(".pdf")]

    def has_knowledge_base(self) -> bool:
        """Check if any PDFs have been processed into the vector database."""
        return self.vectorstore is not None