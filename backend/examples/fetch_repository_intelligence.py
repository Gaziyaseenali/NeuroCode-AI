"""
Example script demonstrating unified repository intelligence aggregation.
Orchestrates metadata, tree, and analysis services for complete repository understanding.
"""
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.intelligence_service import get_intelligence_service


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def main():
    """Demonstrate unified repository intelligence fetching."""
    
    # Example repositories to analyze
    test_repos = [
        "https://github.com/Project-MONAI/MONAI",  # Medical imaging
        "https://github.com/pytorch/pytorch",       # ML framework
        "https://github.com/huggingface/transformers"  # NLP/ML
    ]
    
    # Get intelligence service
    intelligence_service = get_intelligence_service()
    
    for repo_url in test_repos:
        print_section(f"Analyzing: {repo_url}")
        
        try:
            # Fetch unified intelligence
            intelligence = intelligence_service.analyze_repository(
                url=repo_url,
                branch=None,  # Use default branch
                include_filtered=False,
                max_depth=None
            )
            
            # Display metadata summary
            print("📊 METADATA SUMMARY")
            print(f"  Name: {intelligence.metadata.name}")
            print(f"  Description: {intelligence.metadata.description}")
            print(f"  Stars: {intelligence.metadata.stars:,}")
            print(f"  Forks: {intelligence.metadata.forks:,}")
            print(f"  Language: {intelligence.metadata.primary_language}")
            print(f"  Topics: {', '.join(intelligence.metadata.topics[:5])}")
            print(f"  License: {intelligence.metadata.license}")
            
            # Display structure summary
            print("\n📁 STRUCTURE SUMMARY")
            print(f"  Total Files: {intelligence.structure.total_files:,}")
            print(f"  Filtered Files: {intelligence.structure.filtered_files:,}")
            print(f"  Total Directories: {intelligence.structure.total_directories:,}")
            print(f"  Important Files: {sum(intelligence.structure.important_files_count.values())}")
            
            if intelligence.structure.critical_files:
                print(f"\n  Critical Files:")
                for file in intelligence.structure.critical_files[:3]:
                    print(f"    - {file.path}")
            
            # Display classification
            print("\n🏷️  CLASSIFICATION")
            print(f"  Primary Type: {intelligence.classification.primary_type}")
            print(f"  Confidence: {intelligence.classification.confidence}")
            if intelligence.classification.secondary_types:
                print(f"  Secondary Types: {', '.join(intelligence.classification.secondary_types)}")
            
            # Display workflow
            print("\n⚙️  WORKFLOW COMPONENTS")
            print(f"  Training: {'✓' if intelligence.workflow.has_training else '✗'}")
            print(f"  Inference: {'✓' if intelligence.workflow.has_inference else '✗'}")
            print(f"  Preprocessing: {'✓' if intelligence.workflow.has_preprocessing else '✗'}")
            print(f"  Evaluation: {'✓' if intelligence.workflow.has_evaluation else '✗'}")
            print(f"  Deployment: {'✓' if intelligence.workflow.has_deployment else '✗'}")
            
            # Display technology stack
            print("\n🔧 TECHNOLOGY STACK")
            if intelligence.technology.primary_frameworks:
                print(f"  Primary Frameworks: {', '.join(intelligence.technology.primary_frameworks)}")
            if intelligence.technology.medical_frameworks:
                print(f"  Medical Frameworks: {', '.join(intelligence.technology.medical_frameworks)}")
            
            # Display medical AI context
            print("\n🏥 MEDICAL AI CONTEXT")
            print(f"  Is Medical AI: {'Yes' if intelligence.medical_context.is_medical_ai else 'No'}")
            if intelligence.medical_context.is_medical_ai:
                print(f"  Confidence: {intelligence.medical_context.confidence}")
                if intelligence.medical_context.modalities:
                    print(f"  Modalities: {', '.join(intelligence.medical_context.modalities)}")
                if intelligence.medical_context.tasks:
                    print(f"  Tasks: {', '.join(intelligence.medical_context.tasks)}")
            
            # Display statistics
            print("\n📈 STATISTICS")
            print(f"  Python Files: {intelligence.statistics.total_python_files}")
            print(f"  Notebooks: {intelligence.statistics.total_notebook_files}")
            print(f"  Config Files: {intelligence.statistics.total_config_files}")
            print(f"  Has Requirements: {'✓' if intelligence.statistics.has_requirements else '✗'}")
            print(f"  Has Dockerfile: {'✓' if intelligence.statistics.has_dockerfile else '✗'}")
            print(f"  Has README: {'✓' if intelligence.statistics.has_readme else '✗'}")
            print(f"  Has Tests: {'✓' if intelligence.statistics.has_tests else '✗'}")
            print(f"  Has CI/CD: {'✓' if intelligence.statistics.has_ci_cd else '✗'}")
            
            # Display LLM context summary
            print("\n🤖 LLM CONTEXT SUMMARY")
            print(f"  Overview: {intelligence.llm_context.repository_overview}")
            print(f"  Technical: {intelligence.llm_context.technical_summary}")
            
            if intelligence.llm_context.key_capabilities:
                print(f"\n  Key Capabilities:")
                for capability in intelligence.llm_context.key_capabilities:
                    print(f"    - {capability}")
            
            if intelligence.llm_context.suggested_entry_points:
                print(f"\n  Suggested Entry Points:")
                for entry_point in intelligence.llm_context.suggested_entry_points[:5]:
                    print(f"    - {entry_point}")
            
            print(f"\n  Important Files: {intelligence.llm_context.important_files_summary}")
            
            # Display analysis timestamp
            print(f"\n⏰ Analyzed at: {intelligence.analyzed_at}")
            
            # Option to save full JSON
            save_json = input("\n💾 Save full intelligence JSON? (y/n): ").strip().lower()
            if save_json == 'y':
                filename = f"intelligence_{intelligence.owner}_{intelligence.repo}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(intelligence.model_dump(), f, indent=2, ensure_ascii=False)
                print(f"✓ Saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error analyzing repository: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*80)
        
        # Ask if user wants to continue
        if repo_url != test_repos[-1]:
            continue_analysis = input("\nContinue to next repository? (y/n): ").strip().lower()
            if continue_analysis != 'y':
                break


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              Repository Intelligence Aggregation Example                     ║
║                                                                              ║
║  This script demonstrates the unified repository intelligence service that  ║
║  orchestrates metadata fetching, tree analysis, and structure detection.    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    main()
    
    print("\n✨ Example completed!")

# Made with Bob