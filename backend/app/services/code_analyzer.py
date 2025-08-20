"""
Code analysis service for parsing and analyzing code dependencies
"""

import logging
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CodeNode:
    """Represents a code element (class, function, module)"""
    id: str
    name: str
    type: str  # class, function, module, variable
    language: str
    path: str
    line_number: int
    complexity: float = 0.0
    lines_of_code: int = 0
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class CodeDependency:
    """Represents a dependency between code elements"""
    source: str
    target: str
    type: str  # imports, calls, inherits, uses
    weight: float = 1.0
    line_number: Optional[int] = None


class CodeAnalyzer:
    """Service for analyzing code structure and dependencies"""
    
    def __init__(self):
        self.supported_languages = {
            '.py': self._analyze_python,
            '.js': self._analyze_javascript,
            '.ts': self._analyze_typescript,
            '.jsx': self._analyze_jsx,
            '.tsx': self._analyze_tsx,
            '.java': self._analyze_java,
            '.cpp': self._analyze_cpp,
            '.c': self._analyze_c,
            '.cs': self._analyze_csharp,
            '.php': self._analyze_php,
            '.rb': self._analyze_ruby,
            '.go': self._analyze_go,
            '.rs': self._analyze_rust
        }
    
    async def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Analyze an entire project"""
        project_path = Path(project_path)
        
        if not project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")
        
        nodes = []
        edges = []
        
        # Walk through all files in the project
        for file_path in project_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in self.supported_languages:
                try:
                    file_nodes, file_edges = await self.analyze_file(file_path)
                    nodes.extend(file_nodes)
                    edges.extend(file_edges)
                except Exception as e:
                    logger.warning(f"Failed to analyze file {file_path}: {e}")
        
        return {
            "nodes": [node.__dict__ for node in nodes],
            "edges": [edge.__dict__ for edge in edges],
            "metadata": {
                "total_files": len(set(node.path for node in nodes)),
                "total_nodes": len(nodes),
                "total_dependencies": len(edges),
                "languages": list(set(node.language for node in nodes))
            }
        }
    
    async def analyze_file(self, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze a single file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return [], []
        
        # Determine language from file extension
        language = file_path.suffix[1:]  # Remove the dot
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                logger.error(f"Failed to read file {file_path}: {e}")
                return [], []
        
        # Analyze based on language
        analyzer_func = self.supported_languages.get(file_path.suffix)
        if analyzer_func:
            return await analyzer_func(content, file_path)
        else:
            logger.warning(f"Unsupported language for file {file_path}")
            return [], []
    
    async def _analyze_python(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze Python code"""
        nodes = []
        edges = []
        
        try:
            tree = ast.parse(content)
            
            # Extract imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}")
            
            # Extract classes and functions
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_node = CodeNode(
                        id=f"{file_path.stem}.{node.name}",
                        name=node.name,
                        type="class",
                        language="python",
                        path=str(file_path),
                        line_number=node.lineno,
                        complexity=self._calculate_python_complexity(node),
                        lines_of_code=self._count_lines(node)
                    )
                    nodes.append(class_node)
                    
                    # Add inheritance dependencies
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            edges.append(CodeDependency(
                                source=class_node.id,
                                target=base.id,
                                type="inherits",
                                line_number=node.lineno
                            ))
                
                elif isinstance(node, ast.FunctionDef):
                    func_node = CodeNode(
                        id=f"{file_path.stem}.{node.name}",
                        name=node.name,
                        type="function",
                        language="python",
                        path=str(file_path),
                        line_number=node.lineno,
                        complexity=self._calculate_python_complexity(node),
                        lines_of_code=self._count_lines(node)
                    )
                    nodes.append(func_node)
            
            # Add import dependencies
            for imp in imports:
                edges.append(CodeDependency(
                    source=file_path.stem,
                    target=imp,
                    type="imports"
                ))
            
        except SyntaxError as e:
            logger.warning(f"Syntax error in Python file {file_path}: {e}")
        
        return nodes, edges
    
    async def _analyze_javascript(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze JavaScript code"""
        nodes = []
        edges = []
        
        # Simple regex-based analysis for JavaScript
        # In production, you'd use a proper JavaScript parser like esprima
        
        # Extract imports
        import_pattern = r'import\s+(?:{[^}]*}|\*\s+as\s+\w+|\w+)\s+from\s+[\'"`]([^\'"`]+)[\'"`]'
        imports = re.findall(import_pattern, content)
        
        # Extract require statements
        require_pattern = r'require\s*\(\s*[\'"`]([^\'"`]+)[\'"`]'
        requires = re.findall(require_pattern, content)
        
        # Extract function declarations
        function_pattern = r'function\s+(\w+)\s*\('
        functions = re.findall(function_pattern, content)
        
        # Extract class declarations
        class_pattern = r'class\s+(\w+)'
        classes = re.findall(class_pattern, content)
        
        # Create nodes
        for func_name in functions:
            func_node = CodeNode(
                id=f"{file_path.stem}.{func_name}",
                name=func_name,
                type="function",
                language="javascript",
                path=str(file_path),
                line_number=0,  # Would need more sophisticated parsing
                complexity=1.0,
                lines_of_code=0
            )
            nodes.append(func_node)
        
        for class_name in classes:
            class_node = CodeNode(
                id=f"{file_path.stem}.{class_name}",
                name=class_name,
                type="class",
                language="javascript",
                path=str(file_path),
                line_number=0,
                complexity=1.0,
                lines_of_code=0
            )
            nodes.append(class_node)
        
        # Create dependency edges
        for imp in imports + requires:
            edges.append(CodeDependency(
                source=file_path.stem,
                target=imp,
                type="imports"
            ))
        
        return nodes, edges
    
    async def _analyze_typescript(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze TypeScript code (similar to JavaScript for now)"""
        return await self._analyze_javascript(content, file_path)
    
    async def _analyze_jsx(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze JSX code"""
        return await self._analyze_javascript(content, file_path)
    
    async def _analyze_tsx(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze TSX code"""
        return await self._analyze_typescript(content, file_path)
    
    async def _analyze_java(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze Java code"""
        # Placeholder implementation
        return [], []
    
    async def _analyze_cpp(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze C++ code"""
        # Placeholder implementation
        return [], []
    
    async def _analyze_c(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze C code"""
        # Placeholder implementation
        return [], []
    
    async def _analyze_csharp(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze C# code"""
        # Placeholder implementation
        return [], []
    
    async def _analyze_php(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze PHP code"""
        # Placeholder implementation
        return [], []
    
    async def _analyze_ruby(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze Ruby code"""
        # Placeholder implementation
        return [], []
    
    async def _analyze_go(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze Go code"""
        # Placeholder implementation
        return [], []
    
    async def _analyze_rust(self, content: str, file_path: Path) -> Tuple[List[CodeNode], List[CodeDependency]]:
        """Analyze Rust code"""
        # Placeholder implementation
        return [], []
    
    def _calculate_python_complexity(self, node: ast.AST) -> float:
        """Calculate cyclomatic complexity for Python AST node"""
        complexity = 1.0
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1.0
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1.0
            elif isinstance(child, ast.With):
                complexity += 1.0
            elif isinstance(child, ast.Assert):
                complexity += 1.0
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _count_lines(self, node: ast.AST) -> int:
        """Count lines of code for an AST node"""
        if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
            return node.end_lineno - node.lineno + 1
        return 1