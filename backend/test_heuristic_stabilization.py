"""
Test suite for heuristic stabilization patch.
Validates that false positives are reduced while preserving medical AI detection.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.repository_analyzer import RepositoryAnalyzer
from app.models.github import RepositoryTree, TreeNode
from app.models.analyzer import RepositoryType


def create_mock_tree(owner: str, repo: str, files: list) -> RepositoryTree:
    """Create a mock repository tree for testing."""
    tree_nodes = [
        TreeNode(
            path=f,
            name=os.path.basename(f),
            type='file',
            size=1000,
            sha='mock_sha'
        )
        for f in files
    ]
    
    return RepositoryTree(
        owner=owner,
        repo=repo,
        branch='main',
        files=tree_nodes,
        directories=[],
        total_files=len(files),
        total_directories=0,
        filtered_files=0,
        filtered_directories=0,
        important_files={}
    )


def test_linux_kernel():
    """Test that Linux kernel is NOT classified as AI/ML."""
    print("\n=== Testing torvalds/linux ===")
    
    files = [
        'kernel/sched/core.c',
        'kernel/sched/fair.c',
        'kernel/sched/rt.c',
        'drivers/gpu/drm/i915/i915_drv.c',
        'fs/ext4/super.c',
        'net/ipv4/tcp.c',
        'mm/memory.c',
        'arch/x86/kernel/process.c',
        'include/linux/sched.h',
        'Makefile',
        'README',
        'COPYING',
        'Documentation/admin-guide/README.rst',
        'tools/testing/selftests/bpf/test_verifier.c'
    ]
    
    tree = create_mock_tree('torvalds', 'linux', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    primary_type = result.repository_types[0].type if result.repository_types else None
    
    print(f"Primary classification: {primary_type}")
    print(f"All classifications: {[t.type.value for t in result.repository_types]}")
    
    # Should NOT be classified as AI/ML domains
    ai_domains = [
        RepositoryType.NLP,
        RepositoryType.COMPUTER_VISION,
        RepositoryType.REINFORCEMENT_LEARNING,
        RepositoryType.MEDICAL_IMAGING
    ]
    
    detected_ai = [t.type for t in result.repository_types if t.type in ai_domains]
    
    if detected_ai:
        print(f"❌ FAILED: Linux kernel incorrectly classified as: {[d.value for d in detected_ai]}")
        return False
    else:
        print("✅ PASSED: Linux kernel correctly NOT classified as AI/ML")
        return True


def test_react():
    """Test that React is NOT classified as AI/ML."""
    print("\n=== Testing facebook/react ===")
    
    files = [
        'packages/react/src/React.js',
        'packages/react-dom/src/client/ReactDOM.js',
        'packages/scheduler/src/Scheduler.js',
        'packages/react-reconciler/src/ReactFiberWorkLoop.js',
        'scripts/rollup/build.js',
        'README.md',
        'LICENSE',
        'package.json',
        'yarn.lock',
        '.github/workflows/ci.yml',
        'fixtures/dom/src/components/App.js'
    ]
    
    tree = create_mock_tree('facebook', 'react', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    primary_type = result.repository_types[0].type if result.repository_types else None
    
    print(f"Primary classification: {primary_type}")
    print(f"All classifications: {[t.type.value for t in result.repository_types]}")
    
    # Should NOT be classified as AI/ML domains
    ai_domains = [
        RepositoryType.NLP,
        RepositoryType.COMPUTER_VISION,
        RepositoryType.REINFORCEMENT_LEARNING,
        RepositoryType.MEDICAL_IMAGING
    ]
    
    detected_ai = [t.type for t in result.repository_types if t.type in ai_domains]
    
    if detected_ai:
        print(f"❌ FAILED: React incorrectly classified as: {[d.value for d in detected_ai]}")
        return False
    else:
        print("✅ PASSED: React correctly NOT classified as AI/ML")
        return True


def test_fastapi():
    """Test that FastAPI is NOT classified as AI/ML."""
    print("\n=== Testing fastapi/fastapi ===")
    
    files = [
        'fastapi/applications.py',
        'fastapi/routing.py',
        'fastapi/params.py',
        'fastapi/dependencies/utils.py',
        'tests/test_tutorial/test_path_params.py',
        'docs/en/docs/tutorial/first-steps.md',
        'README.md',
        'pyproject.toml',
        'requirements.txt',
        'setup.py'
    ]
    
    tree = create_mock_tree('fastapi', 'fastapi', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    primary_type = result.repository_types[0].type if result.repository_types else None
    
    print(f"Primary classification: {primary_type}")
    print(f"All classifications: {[t.type.value for t in result.repository_types]}")
    
    # Should NOT be classified as AI/ML domains
    ai_domains = [
        RepositoryType.NLP,
        RepositoryType.COMPUTER_VISION,
        RepositoryType.REINFORCEMENT_LEARNING,
        RepositoryType.MEDICAL_IMAGING
    ]
    
    detected_ai = [t.type for t in result.repository_types if t.type in ai_domains]
    
    if detected_ai:
        print(f"❌ FAILED: FastAPI incorrectly classified as: {[d.value for d in detected_ai]}")
        return False
    else:
        print("✅ PASSED: FastAPI correctly NOT classified as AI/ML")
        return True


def test_transformers():
    """Test that Transformers library IS correctly classified as NLP."""
    print("\n=== Testing huggingface/transformers ===")
    
    files = [
        'src/transformers/models/bert/modeling_bert.py',
        'src/transformers/models/gpt2/modeling_gpt2.py',
        'src/transformers/tokenization_utils.py',
        'src/transformers/trainer.py',
        'examples/pytorch/text-classification/run_glue.py',
        'requirements.txt',
        'setup.py',
        'README.md',
        'tests/models/bert/test_modeling_bert.py'
    ]
    
    tree = create_mock_tree('huggingface', 'transformers', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    primary_type = result.repository_types[0].type if result.repository_types else None
    
    print(f"Primary classification: {primary_type}")
    print(f"All classifications: {[t.type.value for t in result.repository_types]}")
    
    # Should be classified as NLP
    is_nlp = any(t.type == RepositoryType.NLP for t in result.repository_types)
    
    if is_nlp:
        print("✅ PASSED: Transformers correctly classified as NLP")
        return True
    else:
        print("❌ FAILED: Transformers NOT classified as NLP")
        return False


def test_monai():
    """Test that MONAI IS correctly classified as Medical AI."""
    print("\n=== Testing Project-MONAI/MONAI ===")
    
    files = [
        'monai/networks/nets/unet.py',
        'monai/transforms/intensity/array.py',
        'monai/data/nifti_reader.py',
        'monai/losses/dice.py',
        'monai/metrics/meandice.py',
        'examples/segmentation/unet_training_dict.py',
        'requirements.txt',
        'setup.py',
        'README.md',
        'tests/test_unet.py',
        'tutorials/3d_segmentation/spleen_segmentation_3d.ipynb'
    ]
    
    tree = create_mock_tree('Project-MONAI', 'MONAI', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    primary_type = result.repository_types[0].type if result.repository_types else None
    
    print(f"Primary classification: {primary_type}")
    print(f"All classifications: {[t.type.value for t in result.repository_types]}")
    print(f"Medical signals: {[s.signal.value for s in result.medical_signals]}")
    
    # Should be classified as Medical Imaging
    is_medical = any(t.type == RepositoryType.MEDICAL_IMAGING for t in result.repository_types)
    
    if is_medical:
        print("✅ PASSED: MONAI correctly classified as Medical AI")
        return True
    else:
        print("❌ FAILED: MONAI NOT classified as Medical AI")
        return False


def test_generic_rl_keywords():
    """Test that generic 'agent' and 'policy' keywords don't trigger RL classification."""
    print("\n=== Testing generic agent/policy keywords ===")
    
    files = [
        'src/user_agent.py',
        'src/policy_manager.py',
        'src/agent_handler.py',
        'docs/agent_architecture.md',
        'README.md',
        'setup.py'
    ]
    
    tree = create_mock_tree('test', 'generic-agent', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    primary_type = result.repository_types[0].type if result.repository_types else None
    
    print(f"Primary classification: {primary_type}")
    print(f"All classifications: {[t.type.value for t in result.repository_types]}")
    
    # Should NOT be classified as RL
    is_rl = any(t.type == RepositoryType.REINFORCEMENT_LEARNING for t in result.repository_types)
    
    if is_rl:
        print("❌ FAILED: Generic agent/policy incorrectly classified as RL")
        return False
    else:
        print("✅ PASSED: Generic agent/policy correctly NOT classified as RL")
        return True


def test_actual_rl_project():
    """Test that actual RL project IS correctly classified."""
    print("\n=== Testing actual RL project ===")
    
    files = [
        'src/agent_train.py',
        'src/environment.py',
        'src/replay_buffer.py',
        'src/dqn_agent.py',
        'src/ppo_trainer.py',
        'requirements.txt',  # Would contain gym, stable-baselines3
        'README.md',
        'configs/dqn_config.yaml'
    ]
    
    tree = create_mock_tree('test', 'rl-project', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    primary_type = result.repository_types[0].type if result.repository_types else None
    
    print(f"Primary classification: {primary_type}")
    print(f"All classifications: {[t.type.value for t in result.repository_types]}")
    
    # Should be classified as RL (has strong RL file patterns)
    is_rl = any(t.type == RepositoryType.REINFORCEMENT_LEARNING for t in result.repository_types)
    
    if is_rl:
        print("✅ PASSED: Actual RL project correctly classified as RL")
        return True
    else:
        print("❌ FAILED: Actual RL project NOT classified as RL")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("HEURISTIC STABILIZATION PATCH TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Linux Kernel (No False Positive)", test_linux_kernel),
        ("React (No False Positive)", test_react),
        ("FastAPI (No False Positive)", test_fastapi),
        ("Transformers (Preserve NLP)", test_transformers),
        ("MONAI (Preserve Medical AI)", test_monai),
        ("Generic Agent Keywords (No False Positive)", test_generic_rl_keywords),
        ("Actual RL Project (Correct Detection)", test_actual_rl_project),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ ERROR in {name}: {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED! Stabilization patch is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Review needed.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

# Made with Bob
