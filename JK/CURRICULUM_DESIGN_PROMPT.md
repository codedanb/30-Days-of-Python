# Master Curriculum Design Prompt

**Goal**: Generate a comprehensive, split-level curriculum for a specific technology (e.g., Python, SQL, LangChain) that ranges from "Absolute Zero" to "PhD/Research Level".

**Output Format**:
For each technology, generating 5 separate Markdown documents:
1.  `<folder/topic_name>_01_BASICS.md`
2.  `<folder/topic_name>_02_INTERMEDIATE.md`
3.  `<folder/topic_name>_03_ADVANCED.md`
4.  `<folder/topic_name>_04_ARCHITECT.md`
5.  `<folder/topic_name>_05_RESEARCH_PHD.md`

---

## Level Definitions

### 1. Basics (The "Alphabet")
*Target Audience*: Absolute beginner (Grade school student / Non-technical person).
*   **Philosophy**: Assume NO prior knowledge. Explain "what" and "why" before "how".
*   **Content Scope**:
    *   Installation & Setup.
    *   Fundamental Syntax & Keywords.
    *   Basic Data Types (Int, String, etc.).
    *   Simple Logic (If/Else, Loops).
    *   *Analogy-heavy explanations.*

### 2. Intermediate (The "Practitioner")
*Target Audience*: Junior Developer / Daily User.
*   **Philosophy**: Focus on "Getting things done". Standard patterns and libraries.
*   **Content Scope**:
    *   Standard Library usage.
    *   Common Data Structures (Lists, Dicts, Trees basics).
    *   Modular programming (Functions, basic OOP).
    *   Error Handling (Try/Except).
    *   File I/O.

### 3. Advanced (The "Senior Engineer")
*Target Audience*: Senior Platform Engineer / Tech Lead.
*   **Philosophy**: Focus on "Optimization, Best Practices, and Internals".
*   **Content Scope**:
    *   Concurrency (Threading, AsyncIO implementation).
    *   Metaprogramming (Decorators, Context Managers).
    *   Design Patterns specific to the language.
    *   Tooling & Linting ecosystems.
    *   Memory profiling basics.

### 4. Architect (The "Principal Principal")
*Target Audience*: Staff Engineer / System Architect.
*   **Philosophy**: Focus on "Design choices, Trade-offs, and Systems Theory".
*   **Content Scope**:
    *   **Internals Deep Dive**: Memory layout (C-Structs), Garbage Collection algorithms.
    *   **Compiler/Interpreter Theory**: Bytecode analysis, AST transformations.
    *   **Scalability**: Distributed system implications, GIL workarounds (C-Extensions).
    *   **Language Design**: Why was this feature implemented this way? (PEP analysis).

### 5. Research / PhD (The "Academic / Pioneer")
*Target Audience*: Researcher, Language Designer, Core Contributor.
*   **Philosophy**: Focus on "Theoretical Foundations, Formal Proofs, and Cutting Edge".
*   **Content Scope**:
    *   **Theoretical CS**: Type Theory, Category Theory applications.
    *   **Comparative Analysis**: JIT strategies (PyPy vs CPython vs GraalPython).
    *   **Novel Optimization Techniques**: Auto-differentiation implementation logs.
    *   **Seminal Papers**: References to original whitepapers defining the tech.
    *   **Mathematical Proofs**: Correctness of algorithms used in standard library (e.g., Timsort stability proof).

---

## Instructions for Generation
For the given Topic (e.g., `{TOPIC_NAME}`):
1.  **Thinking Phase**: Adopt the persona of a Domain Expert & Academic Researcher.
2.  **Drafting**: Create the 5 separate files.
3.  **Granularity**: Do not just list "Sorting". List "Merge Sort vs Timsort: Adaptive Merging strategies and Galloping mode analysis."
4.  **No Code Bloat**: Focus on *Topics* and *Concepts* (the syllabus), not filling it with implementation code yet.


these are the folder/topics you need to create 
Agents
Agile
Algorithms
Architectures
AWS
AZURE
DataBases
Databricks
DataStructures
DesignPatterns
DevOps
FastAPI
GCP
GenAI
GitAndGitHub
Jenkins
JFrog
LangChain
LangGraph
LeetCode
MCP
ML
mlflow
ObjectOrientedDesign
pandas
pydantic
pySpark
Python
SQL
sqlalchemy
SystemDesign
TensorFlow
UIUX
UnitTesting
WebDevelopment

and this list is not exhaustive you may need to add more folder around these, keep the folders under JK folder only as it is the parent folder.