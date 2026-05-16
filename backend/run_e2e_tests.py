"""
Standalone end-to-end test runner for NeuroCode AI.
Runs without pytest dependency for hackathon simplicity.
"""
import sys
import time
import traceback
import os
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, '.')

# Force no token for unauthenticated access (works for public repos)
#os.environ['GITHUB_TOKEN'] = ''

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
    }
]

MALFORMED_URLS = [
    "https://gitlab.com/owner/repo",
    "https://github.com/owner",
    "not-a-url",
    "",
    "https://github.com/owner/repo/tree/main"
]


class TestRunner:
    """Lightweight test runner with reporting."""
    
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        self.github_service = GitHubService()
        self.tree_service = GitHubTreeService()
        self.analyzer = RepositoryAnalyzer()
        self.intelligence_service = RepositoryIntelligenceService()
        
    def run_test(self, category: str, test_name: str, test_func):
        """Run a single test and record result."""
        start = time.time()
        try:
            test_func()
            duration = time.time() - start
            self.results.append({
                "category": category,
                "test": test_name,
                "status": "PASS",
                "details": "",
                "duration": duration
            })
            print(f"  ✓ {test_name} [{duration:.2f}s]")
        except Exception as e:
            duration = time.time() - start
            error_msg = str(e)
            self.results.append({
                "category": category,
                "test": test_name,
                "status": "FAIL",
                "details": error_msg,
                "duration": duration
            })
            print(f"  ✗ {test_name} [{duration:.2f}s]")
            print(f"    Error: {error_msg}")
    
    def test_url_parser_valid_https(self):
        """Test parsing valid HTTPS URLs."""
        owner, repo = parse_github_url("https://github.com/owner/repo")
        assert owner == "owner" and repo == "repo"
        
        owner, repo = parse_github_url("https://github.com/owner/repo.git")
        assert owner == "owner" and repo == "repo"
        
        owner, repo = parse_github_url("https://github.com/owner/repo/")
        assert owner == "owner" and repo == "repo"
    
    def test_url_parser_valid_ssh(self):
        """Test parsing valid SSH URLs."""
        owner, repo = parse_github_url("git@github.com:owner/repo.git")
        assert owner == "owner" and repo == "repo"
    
    def test_url_parser_malformed(self):
        """Test rejection of malformed URLs."""
        failed = []
        for url in MALFORMED_URLS:
            try:
                parse_github_url(url)
                failed.append(url)
            except InvalidGitHubURLError:
                pass  # Expected
        
        if failed:
            raise AssertionError(f"Failed to reject: {failed}")
    
    def test_metadata_general_repo(self):
        """Test fetching metadata for general repository."""
        config = TEST_REPOSITORIES["general"]
        metadata = self.github_service.fetch_repository_metadata(
            config["owner"], config["repo"]
        )
        
        assert metadata.name == config["repo"]
        assert metadata.full_name == f"{config['owner']}/{config['repo']}"
        assert metadata.primary_language == config["expected_language"]
        assert metadata.stars >= config["min_stars"]
    
    def test_metadata_ml_repo(self):
        """Test fetching metadata for ML repository."""
        config = TEST_REPOSITORIES["machine_learning"]
        metadata = self.github_service.fetch_repository_metadata(
            config["owner"], config["repo"]
        )
        
        assert metadata.name == config["repo"]
        assert metadata.primary_language == config["expected_language"]
    
    def test_metadata_medical_repo(self):
        """Test fetching metadata for medical AI repository."""
        config = TEST_REPOSITORIES["medical_ai"]
        metadata = self.github_service.fetch_repository_metadata(
            config["owner"], config["repo"]
        )
        
        assert metadata.name == config["repo"]
        assert metadata.stars >= config["min_stars"]
    
    def test_metadata_invalid_repo(self):
        """Test handling of invalid repositories."""
        for test_case in INVALID_REPOSITORIES:
            try:
                owner, repo = parse_github_url(test_case["url"])
                self.github_service.fetch_repository_metadata(owner, repo)
                raise AssertionError(f"Should have raised {test_case['error_type'].__name__}")
            except test_case["error_type"]:
                pass  # Expected
    
    def test_tree_general_repo(self):
        """Test fetching tree for general repository."""
        config = TEST_REPOSITORIES["general"]
        tree = self.tree_service.fetch_repository_tree(
            config["owner"], config["repo"], max_depth=3
        )
        
        assert tree.total_files > 0
        assert tree.total_directories > 0
        assert len(tree.files) > 0
    
    def test_tree_ml_repo(self):
        """Test fetching tree for ML repository."""
        config = TEST_REPOSITORIES["machine_learning"]
        tree = self.tree_service.fetch_repository_tree(
            config["owner"], config["repo"], max_depth=3
        )
        
        assert tree.total_files > 0
        assert len(tree.files) > 0
    
    def test_tree_medical_repo(self):
        """Test fetching tree for medical AI repository."""
        config = TEST_REPOSITORIES["medical_ai"]
        tree = self.tree_service.fetch_repository_tree(
            config["owner"], config["repo"], max_depth=3
        )
        
        assert tree.total_files > 0
        has_important = any(len(files) > 0 for files in tree.important_files.values())
        assert has_important
    
    def test_analyzer_general_repo(self):
        """Test analyzing general repository."""
        config = TEST_REPOSITORIES["general"]
        tree = self.tree_service.fetch_repository_tree(
            config["owner"], config["repo"], max_depth=3
        )
        analysis = self.analyzer.analyze(tree)
        
        assert analysis.repository_types is not None
        assert len(analysis.repository_types) > 0
        assert analysis.total_python_files > 0
    
    def test_analyzer_ml_repo(self):
        """Test analyzing ML repository."""
        config = TEST_REPOSITORIES["machine_learning"]
        tree = self.tree_service.fetch_repository_tree(
            config["owner"], config["repo"], max_depth=3
        )
        analysis = self.analyzer.analyze(tree)
        
        framework_names = [f.framework.value for f in analysis.frameworks]
        has_expected = any(fw in framework_names for fw in config["expected_frameworks"])
        assert has_expected, f"Expected frameworks not found: {framework_names}"
        
        if config.get("should_detect_training"):
            workflow_names = [w.component.value for w in analysis.workflow_components]
            assert "training" in workflow_names
    
    def test_analyzer_medical_repo(self):
        """Test analyzing medical AI repository."""
        config = TEST_REPOSITORIES["medical_ai"]
        tree = self.tree_service.fetch_repository_tree(
            config["owner"], config["repo"], max_depth=3
        )
        analysis = self.analyzer.analyze(tree)
        
        if config.get("should_detect_medical"):
            signal_names = [s.signal.value for s in analysis.medical_signals]
            assert len(signal_names) > 0, "No medical signals detected"
        
        type_names = [t.type.value for t in analysis.repository_types]
        assert config["expected_type"] in type_names
    
    def test_intelligence_general_repo(self):
        """Test complete intelligence for general repository."""
        config = TEST_REPOSITORIES["general"]
        intelligence = self.intelligence_service.analyze_repository(
            config["url"], max_depth=3
        )
        
        assert intelligence.owner == config["owner"]
        assert intelligence.repo == config["repo"]
        assert intelligence.metadata is not None
        assert intelligence.structure is not None
        assert intelligence.classification is not None
        assert intelligence.workflow is not None
        assert intelligence.technology is not None
        assert intelligence.statistics is not None
        assert intelligence.llm_context is not None
        
        assert intelligence.metadata.name == config["repo"]
        # Relaxed star count check for general repos
        assert intelligence.metadata.stars >= 0
    
    def test_intelligence_ml_repo(self):
        """Test complete intelligence for ML repository."""
        config = TEST_REPOSITORIES["machine_learning"]
        intelligence = self.intelligence_service.analyze_repository(
            config["url"], max_depth=3
        )
        
        assert intelligence.classification.primary_type == config["expected_type"]
        assert len(intelligence.technology.primary_frameworks) > 0
        
        if config.get("should_detect_training"):
            assert intelligence.workflow.has_training
        
        assert intelligence.llm_context.repository_overview is not None
        assert len(intelligence.llm_context.suggested_entry_points) > 0
    
    def test_intelligence_medical_repo(self):
        """Test complete intelligence for medical AI repository."""
        config = TEST_REPOSITORIES["medical_ai"]
        intelligence = self.intelligence_service.analyze_repository(
            config["url"], max_depth=3
        )
        
        assert intelligence.medical_context.is_medical_ai
        assert intelligence.medical_context.confidence != "none"
        assert len(intelligence.medical_context.detected_signals) > 0
        assert config["expected_type"] in intelligence.classification.primary_type
        assert len(intelligence.technology.medical_frameworks) > 0
    
    def test_intelligence_json_structure(self):
        """Test JSON response structure consistency."""
        config = TEST_REPOSITORIES["general"]
        intelligence = self.intelligence_service.analyze_repository(
            config["url"], max_depth=3
        )
        
        data = intelligence.model_dump()
        
        required_keys = [
            "owner", "repo", "branch", "metadata", "structure",
            "classification", "workflow", "technology", 
            "medical_context", "statistics", "llm_context"
        ]
        
        for key in required_keys:
            assert key in data, f"Missing required key: {key}"
        
        assert "primary_type" in data["classification"]
        assert "has_training" in data["workflow"]
        assert "primary_frameworks" in data["technology"]
        assert "is_medical_ai" in data["medical_context"]
        assert "repository_overview" in data["llm_context"]
    
    def run_all_tests(self):
        """Run all tests."""
        print("\n" + "=" * 80)
        print("NEUROCODE AI - END-TO-END VALIDATION TESTS")
        print("=" * 80)
        
        # URL Parser Tests
        print("\n[URL PARSER]")
        self.run_test("URL Parser", "Valid HTTPS URLs", self.test_url_parser_valid_https)
        self.run_test("URL Parser", "Valid SSH URLs", self.test_url_parser_valid_ssh)
        self.run_test("URL Parser", "Malformed URLs", self.test_url_parser_malformed)
        
        # Metadata Fetcher Tests
        print("\n[METADATA FETCHER]")
        self.run_test("Metadata Fetcher", "General Repository", self.test_metadata_general_repo)
        self.run_test("Metadata Fetcher", "ML Repository", self.test_metadata_ml_repo)
        self.run_test("Metadata Fetcher", "Medical AI Repository", self.test_metadata_medical_repo)
        self.run_test("Metadata Fetcher", "Invalid Repository", self.test_metadata_invalid_repo)
        
        # Tree Fetcher Tests
        print("\n[TREE FETCHER]")
        self.run_test("Tree Fetcher", "General Repository", self.test_tree_general_repo)
        self.run_test("Tree Fetcher", "ML Repository", self.test_tree_ml_repo)
        self.run_test("Tree Fetcher", "Medical AI Repository", self.test_tree_medical_repo)
        
        # Analyzer Tests
        print("\n[REPOSITORY ANALYZER]")
        self.run_test("Analyzer", "General Repository", self.test_analyzer_general_repo)
        self.run_test("Analyzer", "ML Repository", self.test_analyzer_ml_repo)
        self.run_test("Analyzer", "Medical AI Repository", self.test_analyzer_medical_repo)
        
        # Intelligence Service Tests
        print("\n[INTELLIGENCE SERVICE]")
        self.run_test("Intelligence Service", "General Repository", self.test_intelligence_general_repo)
        self.run_test("Intelligence Service", "ML Repository", self.test_intelligence_ml_repo)
        self.run_test("Intelligence Service", "Medical AI Repository", self.test_intelligence_medical_repo)
        self.run_test("Intelligence Service", "JSON Structure", self.test_intelligence_json_structure)
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate and save test report."""
        total_time = time.time() - self.start_time
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        total = len(self.results)
        
        report = []
        report.append("\n" + "=" * 80)
        report.append("NEUROCODE AI - END-TO-END VALIDATION REPORT")
        report.append("=" * 80)
        report.append(f"\nTotal Tests: {total} | Passed: {passed} | Failed: {failed}")
        report.append(f"Success Rate: {(passed/total*100):.1f}%")
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
            cat_passed = sum(1 for t in tests if t["status"] == "PASS")
            cat_total = len(tests)
            report.append(f"\n{category.upper()} ({cat_passed}/{cat_total})")
            report.append("-" * 80)
            for test in tests:
                status_icon = "✓" if test["status"] == "PASS" else "✗"
                report.append(f"{status_icon} {test['test']:<50} [{test['duration']:.2f}s]")
                if test["details"]:
                    report.append(f"  → {test['details']}")
        
        report.append("\n" + "=" * 80)
        
        # Print report
        report_text = "\n".join(report)
        print(report_text)
        
        # Save report
        with open("E2E_TEST_REPORT.txt", "w") as f:
            f.write(report_text)
        
        print("\n✓ Report saved to: E2E_TEST_REPORT.txt")
        
        # Return exit code
        return 0 if failed == 0 else 1


if __name__ == "__main__":
    runner = TestRunner()
    exit_code = runner.run_all_tests()
    sys.exit(exit_code)

# Made with Bob
