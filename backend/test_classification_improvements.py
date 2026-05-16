"""
Test script to verify improved classification system.
Tests with example repositories: Transformers, SAM, MONAI, Ultralytics
"""
import sys
from app.models.github import RepositoryTree, TreeNode
from app.services.repository_analyzer import RepositoryAnalyzer

def create_mock_tree(owner: str, repo: str, files: list) -> RepositoryTree:
    """Create a mock repository tree for testing."""
    tree_nodes = [
        TreeNode(
            path=f,
            name=f.split('/')[-1],
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
        sha='mock_sha',
        files=tree_nodes,
        directories=[],
        total_files=len(files),
        total_directories=0,
        filtered_files=len(files),
        filtered_directories=0,
        important_files={}
    )

def test_transformers_classification():
    """Test Transformers repository - should be NLP/Foundation Models/Multimodal AI"""
    print("\n=== Testing Transformers Repository ===")
    files = [
        'src/transformers/models/bert/modeling_bert.py',
        'src/transformers/models/gpt2/modeling_gpt2.py',
        'src/transformers/tokenization_utils.py',
        'src/transformers/trainer.py',
        'examples/pytorch/language-modeling/run_clm.py',
        'examples/pytorch/text-classification/run_glue.py',
        'src/transformers/pipelines/text_generation.py',
        'src/transformers/models/clip/modeling_clip.py',
        'README.md',
        'requirements.txt'
    ]
    
    tree = create_mock_tree('huggingface', 'transformers', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    print(f"Primary Type: {result.repository_types[0].type.value}")
    print(f"Confidence: {result.repository_types[0].confidence.value}")
    print(f"Score: {result.repository_types[0].score:.2f}")
    print(f"Explanation: {result.repository_types[0].explanation}")
    print(f"\nAll Classifications:")
    for i, rt in enumerate(result.repository_types[:3], 1):
        print(f"  {i}. {rt.type.value} ({rt.confidence.value}, score: {rt.score:.2f})")
    
    # Verify expectations
    primary_types = [rt.type.value for rt in result.repository_types[:3]]
    assert 'nlp' in primary_types or 'foundation_models' in primary_types, \
        f"Expected NLP or Foundation Models, got: {primary_types}"
    print("✓ PASSED: Correctly classified as NLP/Foundation Models")

def test_segment_anything_classification():
    """Test Segment Anything - should be Computer Vision/Segmentation, NOT Medical Imaging"""
    print("\n=== Testing Segment Anything Repository ===")
    files = [
        'segment_anything/modeling/sam.py',
        'segment_anything/modeling/image_encoder.py',
        'segment_anything/modeling/mask_decoder.py',
        'segment_anything/predictor.py',
        'segment_anything/automatic_mask_generator.py',
        'notebooks/predictor_example.ipynb',
        'scripts/amg.py',
        'demo/app.py',
        'README.md',
        'requirements.txt'
    ]
    
    tree = create_mock_tree('facebookresearch', 'segment-anything', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    print(f"Primary Type: {result.repository_types[0].type.value}")
    print(f"Confidence: {result.repository_types[0].confidence.value}")
    print(f"Score: {result.repository_types[0].score:.2f}")
    print(f"Explanation: {result.repository_types[0].explanation}")
    print(f"\nAll Classifications:")
    for i, rt in enumerate(result.repository_types[:3], 1):
        print(f"  {i}. {rt.type.value} ({rt.confidence.value}, score: {rt.score:.2f})")
    
    # Verify expectations
    primary_type = result.repository_types[0].type.value
    assert primary_type in ['computer_vision', 'segmentation'], \
        f"Expected Computer Vision or Segmentation, got: {primary_type}"
    assert primary_type != 'medical_imaging', \
        f"Should NOT be classified as Medical Imaging"
    print("✓ PASSED: Correctly classified as Computer Vision/Segmentation (NOT Medical Imaging)")

def test_monai_classification():
    """Test MONAI - should be Medical Imaging with high confidence"""
    print("\n=== Testing MONAI Repository ===")
    files = [
        'monai/networks/nets/unet.py',
        'monai/transforms/intensity/array.py',
        'monai/data/nifti_reader.py',
        'monai/data/itk_reader.py',
        'monai/apps/deepgrow/interaction.py',
        'monai/losses/dice.py',
        'examples/segmentation/unet_training_dict.py',
        'tutorials/3d_segmentation/spleen_segmentation_3d.ipynb',
        'monai/data/decathlon_datalist.py',
        'tests/test_load_image.py',
        'README.md',
        'requirements.txt',
        'setup.py'
    ]
    
    tree = create_mock_tree('Project-MONAI', 'MONAI', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    print(f"Primary Type: {result.repository_types[0].type.value}")
    print(f"Confidence: {result.repository_types[0].confidence.value}")
    print(f"Score: {result.repository_types[0].score:.2f}")
    print(f"Explanation: {result.repository_types[0].explanation}")
    print(f"\nAll Classifications:")
    for i, rt in enumerate(result.repository_types[:3], 1):
        print(f"  {i}. {rt.type.value} ({rt.confidence.value}, score: {rt.score:.2f})")
    
    # Verify expectations
    primary_type = result.repository_types[0].type.value
    assert primary_type == 'medical_imaging', \
        f"Expected Medical Imaging, got: {primary_type}"
    assert result.repository_types[0].confidence.value == 'high', \
        f"Expected high confidence for MONAI"
    print("✓ PASSED: Correctly classified as Medical Imaging with high confidence")

def test_ultralytics_classification():
    """Test Ultralytics YOLO - should be Object Detection/Computer Vision"""
    print("\n=== Testing Ultralytics YOLO Repository ===")
    files = [
        'ultralytics/models/yolo/detect/train.py',
        'ultralytics/models/yolo/detect/predict.py',
        'ultralytics/models/yolo/detect/val.py',
        'ultralytics/nn/modules/head.py',
        'ultralytics/nn/modules/conv.py',
        'ultralytics/utils/ops.py',
        'ultralytics/data/augment.py',
        'ultralytics/data/dataset.py',
        'ultralytics/engine/trainer.py',
        'ultralytics/engine/predictor.py',
        'examples/YOLOv8-ONNXRuntime/main.py',
        'README.md',
        'requirements.txt'
    ]
    
    tree = create_mock_tree('ultralytics', 'ultralytics', files)
    analyzer = RepositoryAnalyzer()
    result = analyzer.analyze(tree)
    
    print(f"Primary Type: {result.repository_types[0].type.value}")
    print(f"Confidence: {result.repository_types[0].confidence.value}")
    print(f"Score: {result.repository_types[0].score:.2f}")
    print(f"Explanation: {result.repository_types[0].explanation}")
    print(f"\nAll Classifications:")
    for i, rt in enumerate(result.repository_types[:3], 1):
        print(f"  {i}. {rt.type.value} ({rt.confidence.value}, score: {rt.score:.2f})")
    
    # Verify expectations
    primary_types = [rt.type.value for rt in result.repository_types[:2]]
    assert 'object_detection' in primary_types or 'computer_vision' in primary_types, \
        f"Expected Object Detection or Computer Vision, got: {primary_types}"
    print("✓ PASSED: Correctly classified as Object Detection/Computer Vision")

def main():
    """Run all classification tests."""
    print("=" * 70)
    print("Testing Improved Repository Classification System")
    print("=" * 70)
    
    try:
        test_transformers_classification()
        test_segment_anything_classification()
        test_monai_classification()
        test_ultralytics_classification()
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED!")
        print("=" * 70)
        return 0
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())

# Made with Bob
