import asyncio
import aiohttp
import time
import json
from statistics import mean, median
from collections import defaultdict


class StressTester:
  def __init__(self, url, concurrent=10, timeout=10):
    self.url = url
    self.concurrent = concurrent
    self.timeout = timeout
    self.results = []
  
  async def post_request(self, session, payload):
    start = time.time()
    try:
      async with session.post(self.url, json=payload, timeout=self.timeout) as response:
        await response.text()
        return {
          'success': True,
          'status': response.status,
          'time': time.time() - start,
          'payload': payload
        }
    except Exception as e:
      return {
        'success': False,
        'error': str(e),
        'time': time.time() - start,
        'payload': payload
      }
  
  async def run_batch(self, payloads):
    async with aiohttp.ClientSession() as session:
      tasks = [self.post_request(session, p) for p in payloads]
      return await asyncio.gather(*tasks)
  
  async def stress_test(self, payload_list):
    print(f"🚀 Testing {len(payload_list)} requests with {self.concurrent} concurrent")
    
    # Split into batches
    batches = [payload_list[i:i + self.concurrent]
               for i in range(0, len(payload_list), self.concurrent)]
    
    start_time = time.time()
    
    for i, batch in enumerate(batches):
      batch_results = await self.run_batch(batch)
      self.results.extend(batch_results)
      
      # Progress update
      completed = len(self.results)
      success_rate = sum(1 for r in self.results if r['success']) / completed * 100
      print(f"Batch {i + 1}/{len(batches)} | {completed}/{len(payload_list)} | "
            f"Success: {success_rate:.1f}%")
    
    self.print_stats(time.time() - start_time)
  
  def print_stats(self, total_time):
    successful = [r for r in self.results if r['success']]
    failed = [r for r in self.results if not r['success']]
    times = [r['time'] * 1000 for r in self.results]  # Convert to ms
    
    print(f"\n📊 RESULTS:")
    print(f"Total: {len(self.results)} | Success: {len(successful)} | Failed: {len(failed)}")
    print(f"Success Rate: {len(successful) / len(self.results) * 100:.1f}%")
    print(f"Total Time: {total_time:.2f}s | RPS: {len(self.results) / total_time:.1f}")
    
    if times:
      print(f"Response Times - Avg: {mean(times):.0f}ms | "
            f"Min: {min(times):.0f}ms | Max: {max(times):.0f}ms")
    
    # Status codes
    status_counts = defaultdict(int)
    for r in successful:
      status_counts[r['status']] += 1
    if status_counts:
      print(f"Status Codes: {dict(status_counts)}")
    
    # Error summary
    if failed:
      error_counts = defaultdict(int)
      for r in failed:
        error_counts[r['error']] += 1
      print(f"Errors: {dict(error_counts)}")


# Usage example
async def main(url, payloads):
 
  tester = StressTester(
    url=url,
    concurrent=5,
    timeout=10
  )
  
  await tester.stress_test(payloads)



