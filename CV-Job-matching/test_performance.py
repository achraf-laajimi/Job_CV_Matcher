# test_performance.py
"""
Quick test to demonstrate optimization improvements
"""
import time
from app.pipeline import run_pipeline, clear_cache
from pathlib import Path

def test_with_cache():
    """Test the same CV twice to show cache effectiveness"""
    
    cv_path = "app/data/cv_ahmed.pdf"  # Use first CV
    jd_text = "Looking for Python developer with 5 years experience"
    
    if not Path(cv_path).exists():
        print("❌ CV file not found")
        return
    
    # Clear cache first
    print("🗑️  Clearing cache...")
    clear_cache()
    
    # First run (no cache)
    print("\n" + "="*60)
    print("🔄 RUN 1: Without Cache")
    print("="*60)
    start = time.time()
    result1 = run_pipeline(cv_path, jd_text)
    time1 = time.time() - start
    print(f"⏱️  Time: {time1:.2f}s")
    
    # Second run (with cache)
    print("\n" + "="*60)
    print("🚀 RUN 2: With Cache")
    print("="*60)
    start = time.time()
    result2 = run_pipeline(cv_path, jd_text)
    time2 = time.time() - start
    print(f"⏱️  Time: {time2:.2f}s")
    
    # Show improvement
    print("\n" + "="*60)
    print("📊 PERFORMANCE IMPROVEMENT")
    print("="*60)
    speedup = time1 / time2 if time2 > 0 else 0
    print(f"First run:  {time1:.2f}s")
    print(f"Second run: {time2:.2f}s")
    print(f"Speedup:    {speedup:.2f}× faster! 🚀")
    print(f"Time saved: {time1 - time2:.2f}s")
    
    if speedup > 2:
        print("\n✅ Cache is working perfectly!")
    elif speedup > 1.5:
        print("\n✅ Cache is working well!")
    else:
        print("\n⚠️  Cache might not be fully effective")

if __name__ == "__main__":
    print("\n🧪 Testing Performance Optimizations")
    print("="*60)
    print("This will process the same CV twice:")
    print("1. First run: Full processing (extraction + parsing + scoring)")
    print("2. Second run: With cached CV data")
    print("="*60)
    
    try:
        test_with_cache()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
