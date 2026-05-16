"""
End-to-end integration tests for NeuroCode AI repository intelligence pipeline.
Tests the complete flow from URL parsing to intelligence aggregation.

Optimized for:
- Low RAM usage
- Hackathon-friendly validation
- Quick execution
- Comprehensive coverage
"""
import pytest
import time
from typing import Dict, List, Any
from app.utils.github_parser import parse_github_url, InvalidGitHubURLError
from app.services.github_service import GitHubService, GitHubServiceError, RepositoryNotFoundError
from app.services.github_tree_service import GitHubTreeService, GitHubTreeServiceError
from app.services.repository_analyzer import RepositoryAnalyzer
from app.services.intelligence_service import RepositoryIntelligenceService, IntelligenceServiceError


# Test repository configurations
TEST_REPOSITORIES = {
    "general": {
        "url": "https://github.com/fastapi/fastapi",
        "owner": "fastapi",
        "repo": "fastapi",
        "expected_type": "general",
        "expected_language": "Python",
        "min_stars": 50000,
        "should_have_readme": True,
        "should_have_requirements": True
    },
    "machine_learning": {
        "url": "https://github.com/pytorch/examples",
        "owner": "pytorch",
        "repo": "examples",
        "expected_type": "machine_learning",
        "expected_frameworks": ["pytorch"],
        "expected_language": "Python",
        "should_detect_training": True,
        "should_detect_inference": True
    },
    "medical_ai": {
        "url": "https://github.com/Project-MONAI/MONAI",
        "owner": "Project-MONAI",
        "repo": "MONAI",
        "expected_type": "medical_imaging",
        "expected_frameworks": ["monai", "pytorch"],
        "expected_medical_signals": ["medical_imaging"],
        "should_detect_medical": True,
        "min_stars": 3000
    }
}

INVALID_REPOSITORIES = [
    {
        "url": "https://github.com/nonexistent/repository12345xyz",
        "error_type": RepositoryNotFoundError,
        "description": "Non-existent repository"
    },
    {
        "url": "https://github.com/invalid/private-repo-test-xyz",
        "error_type": RepositoryNotFoundError,
        "description": "Private/inaccessible repository"
    }
]

MALFORMED_URLS = [
    {
        "url": "https://gitlab.com/owner/repo",
        "description": "GitLab URL (not GitHub)"
    },
    {
        "url": "https://github.com/owner",
        "description": "Missing repository name"
    },
    {
        "url": "not-a-url",
        "description": "Invalid URL format"
    },
    {
        "url": "",
        "description": "Empty URL"
    },
    {
        "url": "https://github.com/owner/repo/tree/main",
        "description": "URL with branch path"
    }
]


class TestReport:
    """Lightweight test report generator."""
    
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        
    def add_result(self, category: str, test_name: str, status: str, 
                   details: str = "", duration: float = 0):
        """Add a test result."""
        self.results.append({
            "category": category,
            "test": test_name,
            "status": status,
            "details": details,
            "duration": duration
        })
    
    def generate_report(self) -> str:
        """Generate a concise validation report."""
        total_time = time.time() - self.start_time
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        total = len(self.results)
        
        report = []
        report.append("=" * 80)
        report.append("NEUROCODE AI - END-TO-END VALIDATION REPORT")
        report.append("=" * 80)
        report.append(f"\nTotal Tests: {total} | Passed: {passed} | Failed: {failed}")
        report.append(f"Total Duration: {total_time:.2f}s")
        report.append("\n" + "=" * 80)
        
        # Group by category
        categories = {}
        for result in self.results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        
        for category, tests in categories.items():
            report.append(f"\n{category.upper()}")
            report.append("-" * 80)
            for test in tests:
                status_icon = "✓" if test["status"] == "PASS" else "✗"
                report.append(f"{status_icon} {test['test']:<50} [{test['duration']:.2f}s]")
                if test["details"]:
                    report.append(f"  → {test['details']}")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)


@pytest.fixture(scope="module")
def test_report():
    """Fixture for test report."""
    return TestReport()


@pytest.fixture(scope="module")
def github_service():
    """Fixture for GitHub service."""
    return GitHubService()


@pytest.fixture(scope="module")
def tree_service():
    """Fixture for GitHub tree service."""
    return GitHubTreeService()


@pytest.fixture(scope="module")
def analyzer():
    """Fixture for repository analyzer."""
    return RepositoryAnalyzer()


@pytest.fixture(scope="module")
def intelligence_service():
    """Fixture for intelligence service."""
    return RepositoryIntelligenceService()


class TestURLParser:
    """Test URL parser functionality."""
    
    def test_valid_https_urls(self, test_report):
        """Test parsing valid HTTPS URLs."""
        start = time.time()
        try:
            # Test standard HTTPS URL
            owner, repo = parse_github_url("https://github.com/owner/repo")
            assert owner == "owner" and repo == "repo"
            
            # Test with .git extension
            owner, repo = parse_github_url("https://github.com/owner/repo.git")
            assert owner == "owner" and repo == "repo"
            
            # Test with trailing slash
            owner, repo = parse_github_url("https://github.com/owner/repo/")
            assert owner == "owner" and repo == "repo"
            
            test_report.add_result("URL Parser", "Valid HTTPS URLs", "PASS", 
                                 "All formats parsed correctly", time.time() - start)
        except Exception as e:
            test_report.add_result("URL Parser", "Valid HTTPS URLs", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_valid_ssh_urls(self, test_report):
        """Test parsing valid SSH URLs."""
        start = time.time()
        try:
            owner, repo = parse_github_url("git@github.com:owner/repo.git")
            assert owner == "owner" and repo == "repo"
            
            test_report.add_result("URL Parser", "Valid SSH URLs", "PASS", 
                                 "SSH format parsed correctly", time.time() - start)
        except Exception as e:
            test_report.add_result("URL Parser", "Valid SSH URLs", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_malformed_urls(self, test_report):
        """Test rejection of malformed URLs."""
        start = time.time()
        failed_urls = []
        
        for test_case in MALFORMED_URLS:
            try:
                parse_github_url(test_case["url"])
                failed_urls.append(test_case["description"])
            except InvalidGitHubURLError:
                pass  # Expected
        
        if failed_urls:
            test_report.add_result("URL Parser", "Malformed URLs", "FAIL", 
                                 f"Failed to reject: {', '.join(failed_urls)}", 
                                 time.time() - start)
            pytest.fail(f"Failed to reject malformed URLs: {failed_urls}")
        else:
            test_report.add_result("URL Parser", "Malformed URLs", "PASS", 
                                 f"All {len(MALFORMED_URLS)} malformed URLs rejected", 
                                 time.time() - start)


class TestMetadataFetcher:
    """Test GitHub metadata fetcher."""
    
    def test_general_repository_metadata(self, github_service, test_report):
        """Test fetching metadata for general repository."""
        start = time.time()
        config = TEST_REPOSITORIES["general"]
        
        try:
            metadata = github_service.fetch_repository_metadata(
                config["owner"], config["repo"]
            )
            
            # Validate basic fields
            assert metadata.name == config["repo"]
            assert metadata.full_name == f"{config['owner']}/{config['repo']}"
            assert metadata.language == config["expected_language"]
            assert metadata.stars >= config["min_stars"]
            assert metadata.html_url is not None
            
            test_report.add_result("Metadata Fetcher", "General Repository", "PASS", 
                                 f"{metadata.stars} stars, {metadata.language}", 
                                 time.time() - start)
        except Exception as e:
            test_report.add_result("Metadata Fetcher", "General Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_ml_repository_metadata(self, github_service, test_report):
        """Test fetching metadata for ML repository."""
        start = time.time()
        config = TEST_REPOSITORIES["machine_learning"]
        
        try:
            metadata = github_service.fetch_repository_metadata(
                config["owner"], config["repo"]
            )
            
            assert metadata.name == config["repo"]
            assert metadata.language == config["expected_language"]
            
            test_report.add_result("Metadata Fetcher", "ML Repository", "PASS", 
                                 f"{metadata.stars} stars", time.time() - start)
        except Exception as e:
            test_report.add_result("Metadata Fetcher", "ML Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_medical_ai_repository_metadata(self, github_service, test_report):
        """Test fetching metadata for medical AI repository."""
        start = time.time()
        config = TEST_REPOSITORIES["medical_ai"]
        
        try:
            metadata = github_service.fetch_repository_metadata(
                config["owner"], config["repo"]
            )
            
            assert metadata.name == config["repo"]
            assert metadata.stars >= config["min_stars"]
            
            test_report.add_result("Metadata Fetcher", "Medical AI Repository", "PASS", 
                                 f"{metadata.stars} stars", time.time() - start)
        except Exception as e:
            test_report.add_result("Metadata Fetcher", "Medical AI Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_invalid_repositories(self, github_service, test_report):
        """Test handling of invalid repositories."""
        start = time.time()
        failed_cases = []
        
        for test_case in INVALID_REPOSITORIES:
            try:
                owner, repo = parse_github_url(test_case["url"])
                github_service.fetch_repository_metadata(owner, repo)
                failed_cases.append(test_case["description"])
            except test_case["error_type"]:
                pass  # Expected
            except Exception as e:
                failed_cases.append(f"{test_case['description']}: {str(e)}")
        
        if failed_cases:
            test_report.add_result("Metadata Fetcher", "Invalid Repositories", "FAIL", 
                                 f"Failed: {', '.join(failed_cases)}", time.time() - start)
            pytest.fail(f"Failed to handle invalid repositories: {failed_cases}")
        else:
            test_report.add_result("Metadata Fetcher", "Invalid Repositories", "PASS", 
                                 f"All {len(INVALID_REPOSITORIES)} invalid repos handled", 
                                 time.time() - start)


class TestTreeFetcher:
    """Test GitHub tree fetcher."""
    
    def test_general_repository_tree(self, tree_service, test_report):
        """Test fetching tree for general repository."""
        start = time.time()
        config = TEST_REPOSITORIES["general"]
        
        try:
            tree = tree_service.fetch_repository_tree(
                config["owner"], config["repo"], max_depth=3
            )
            
            assert tree.total_files > 0
            assert tree.total_directories > 0
            assert len(tree.files) > 0
            assert tree.important_files is not None
            
            test_report.add_result("Tree Fetcher", "General Repository", "PASS", 
                                 f"{tree.total_files} files, {tree.total_directories} dirs", 
                                 time.time() - start)
        except Exception as e:
            test_report.add_result("Tree Fetcher", "General Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_ml_repository_tree(self, tree_service, test_report):
        """Test fetching tree for ML repository."""
        start = time.time()
        config = TEST_REPOSITORIES["machine_learning"]
        
        try:
            tree = tree_service.fetch_repository_tree(
                config["owner"], config["repo"], max_depth=3
            )
            
            assert tree.total_files > 0
            assert len(tree.files) > 0
            
            test_report.add_result("Tree Fetcher", "ML Repository", "PASS", 
                                 f"{tree.total_files} files", time.time() - start)
        except Exception as e:
            test_report.add_result("Tree Fetcher", "ML Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_medical_ai_repository_tree(self, tree_service, test_report):
        """Test fetching tree for medical AI repository."""
        start = time.time()
        config = TEST_REPOSITORIES["medical_ai"]
        
        try:
            tree = tree_service.fetch_repository_tree(
                config["owner"], config["repo"], max_depth=3
            )
            
            assert tree.total_files > 0
            # Check for important files
            has_important = any(
                len(files) > 0 for files in tree.important_files.values()
            )
            assert has_important
            
            test_report.add_result("Tree Fetcher", "Medical AI Repository", "PASS", 
                                 f"{tree.total_files} files", time.time() - start)
        except Exception as e:
            test_report.add_result("Tree Fetcher", "Medical AI Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise


class TestRepositoryAnalyzer:
    """Test repository analyzer."""
    
    def test_general_repository_analysis(self, tree_service, analyzer, test_report):
        """Test analyzing general repository."""
        start = time.time()
        config = TEST_REPOSITORIES["general"]
        
        try:
            tree = tree_service.fetch_repository_tree(
                config["owner"], config["repo"], max_depth=3
            )
            analysis = analyzer.analyze(tree)
            
            assert analysis.repository_types is not None
            assert len(analysis.repository_types) > 0
            assert analysis.total_python_files > 0
            
            test_report.add_result("Analyzer", "General Repository", "PASS", 
                                 f"Type: {analysis.repository_types[0].type.value}", 
                                 time.time() - start)
        except Exception as e:
            test_report.add_result("Analyzer", "General Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_ml_repository_analysis(self, tree_service, analyzer, test_report):
        """Test analyzing ML repository."""
        start = time.time()
        config = TEST_REPOSITORIES["machine_learning"]
        
        try:
            tree = tree_service.fetch_repository_tree(
                config["owner"], config["repo"], max_depth=3
            )
            analysis = analyzer.analyze(tree)
            
            # Check for ML frameworks
            framework_names = [f.framework.value for f in analysis.frameworks]
            has_expected_frameworks = any(
                fw in framework_names for fw in config["expected_frameworks"]
            )
            assert has_expected_frameworks, f"Expected frameworks not found: {framework_names}"
            
            # Check for workflow components
            if config.get("should_detect_training"):
                workflow_names = [w.component.value for w in analysis.workflow_components]
                assert "training" in workflow_names
            
            test_report.add_result("Analyzer", "ML Repository", "PASS", 
                                 f"Frameworks: {', '.join(framework_names[:3])}", 
                                 time.time() - start)
        except Exception as e:
            test_report.add_result("Analyzer", "ML Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_medical_ai_repository_analysis(self, tree_service, analyzer, test_report):
        """Test analyzing medical AI repository."""
        start = time.time()
        config = TEST_REPOSITORIES["medical_ai"]
        
        try:
            tree = tree_service.fetch_repository_tree(
                config["owner"], config["repo"], max_depth=3
            )
            analysis = analyzer.analyze(tree)
            
            # Check for medical signals
            if config.get("should_detect_medical"):
                signal_names = [s.signal.value for s in analysis.medical_signals]
                has_medical_signals = len(signal_names) > 0
                assert has_medical_signals, "No medical signals detected"
            
            # Check repository type
            type_names = [t.type.value for t in analysis.repository_types]
            assert config["expected_type"] in type_names
            
            test_report.add_result("Analyzer", "Medical AI Repository", "PASS", 
                                 f"Type: {type_names[0]}", time.time() - start)
        except Exception as e:
            test_report.add_result("Analyzer", "Medical AI Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise


class TestIntelligenceService:
    """Test complete intelligence service pipeline."""
    
    def test_general_repository_intelligence(self, intelligence_service, test_report):
        """Test complete intelligence for general repository."""
        start = time.time()
        config = TEST_REPOSITORIES["general"]
        
        try:
            intelligence = intelligence_service.analyze_repository(
                config["url"], max_depth=3
            )
            
            # Validate structure
            assert intelligence.owner == config["owner"]
            assert intelligence.repo == config["repo"]
            assert intelligence.metadata is not None
            assert intelligence.structure is not None
            assert intelligence.classification is not None
            assert intelligence.workflow is not None
            assert intelligence.technology is not None
            assert intelligence.statistics is not None
            assert intelligence.llm_context is not None
            
            # Validate metadata
            assert intelligence.metadata.name == config["repo"]
            assert intelligence.metadata.stars >= config["min_stars"]
            
            # Validate statistics
            if config.get("should_have_readme"):
                assert intelligence.statistics.has_readme
            if config.get("should_have_requirements"):
                assert intelligence.statistics.has_requirements
            
            test_report.add_result("Intelligence Service", "General Repository", "PASS", 
                                 f"Complete pipeline: {intelligence.classification.primary_type}", 
                                 time.time() - start)
        except Exception as e:
            test_report.add_result("Intelligence Service", "General Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_ml_repository_intelligence(self, intelligence_service, test_report):
        """Test complete intelligence for ML repository."""
        start = time.time()
        config = TEST_REPOSITORIES["machine_learning"]
        
        try:
            intelligence = intelligence_service.analyze_repository(
                config["url"], max_depth=3
            )
            
            # Validate classification
            assert intelligence.classification.primary_type == config["expected_type"]
            
            # Validate technology stack
            assert len(intelligence.technology.primary_frameworks) > 0
            
            # Validate workflow
            if config.get("should_detect_training"):
                assert intelligence.workflow.has_training
            
            # Validate LLM context
            assert intelligence.llm_context.repository_overview is not None
            assert len(intelligence.llm_context.suggested_entry_points) > 0
            
            test_report.add_result("Intelligence Service", "ML Repository", "PASS", 
                                 f"Frameworks: {', '.join(intelligence.technology.primary_frameworks)}", 
                                 time.time() - start)
        except Exception as e:
            test_report.add_result("Intelligence Service", "ML Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_medical_ai_repository_intelligence(self, intelligence_service, test_report):
        """Test complete intelligence for medical AI repository."""
        start = time.time()
        config = TEST_REPOSITORIES["medical_ai"]
        
        try:
            intelligence = intelligence_service.analyze_repository(
                config["url"], max_depth=3
            )
            
            # Validate medical context
            assert intelligence.medical_context.is_medical_ai
            assert intelligence.medical_context.confidence != "none"
            assert len(intelligence.medical_context.detected_signals) > 0
            
            # Validate classification
            assert config["expected_type"] in intelligence.classification.primary_type
            
            # Validate technology
            has_medical_frameworks = len(intelligence.technology.medical_frameworks) > 0
            assert has_medical_frameworks
            
            test_report.add_result("Intelligence Service", "Medical AI Repository", "PASS", 
                                 f"Medical: {intelligence.medical_context.confidence} confidence", 
                                 time.time() - start)
        except Exception as e:
            test_report.add_result("Intelligence Service", "Medical AI Repository", "FAIL", 
                                 str(e), time.time() - start)
            raise
    
    def test_json_response_structure(self, intelligence_service, test_report):
        """Test JSON response structure consistency."""
        start = time.time()
        config = TEST_REPOSITORIES["general"]
        
        try:
            intelligence = intelligence_service.analyze_repository(
                config["url"], max_depth=3
            )
            
            # Convert to dict (Pydantic model)
            data = intelligence.model_dump()
            
            # Validate required top-level keys
            required_keys = [
                "owner", "repo", "branch", "metadata", "structure",
                "classification", "workflow", "technology", 
                "medical_context", "statistics", "llm_context"
            ]
            
            for key in required_keys:
                assert key in data, f"Missing required key: {key}"
            
            # Validate nested structures
            assert "primary_type" in data["classification"]
            assert "has_training" in data["workflow"]
            assert "primary_frameworks" in data["technology"]
            assert "is_medical_ai" in data["medical_context"]
            assert "repository_overview" in data["llm_context"]
            
            test_report.add_result("Intelligence Service", "JSON Structure", "PASS", 
                                 f"All {len(required_keys)} required keys present", 
                                 time.time() - start)
        except Exception as e:
            test_report.add_result("Intelligence Service", "JSON Structure", "FAIL", 
                                 str(e), time.time() - start)
            raise


def test_generate_report(test_report):
    """Generate and print final test report."""
    report = test_report.generate_report()
    print("\n" + report)
    
    # Save report to file
    with open("backend/E2E_TEST_REPORT.txt", "w") as f:
        f.write(report)
    
    print("\n✓ Report saved to: backend/E2E_TEST_REPORT.txt")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

# Made with Bob
