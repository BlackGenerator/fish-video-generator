<template>
  <div id="app">
    <header>
      <h1>🐟 Fish Video Generator</h1>
      <p>Generate narrated videos from text — no GPU required</p>
    </header>

    <main>
      <div class="container">
        <textarea 
          v-model="prompt" 
          placeholder="Describe your video (e.g., 'A robot dancing in Tokyo')"
          rows="4"
        ></textarea>
        
        <div class="controls">
          <input 
            type="number" 
            v-model.number="duration" 
            min="5" 
            max="60"
            placeholder="Duration (seconds)"
          >
          <button @click="generateVideo" :disabled="loading">
            {{ loading ? 'Generating...' : 'Create Video' }}
          </button>
        </div>

        <div v-if="error" class="error">{{ error }}</div>

        <div v-if="videoUrl" class="result">
          <h3>Your Video:</h3>
          <video controls :src="videoUrl"></video>
          <a :href="videoUrl" download>Download MP4</a>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      prompt: '',
      duration: 10,
      loading: false,
      videoUrl: null,
      error: null
    }
  },
  methods: {
    async generateVideo() {
      if (!this.prompt.trim()) {
        this.error = 'Please enter a description';
        return;
      }

      this.loading = true;
      this.error = null;
      this.videoUrl = null;

      try {
        const response = await fetch('http://localhost:8000/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            prompt: this.prompt, 
            duration: this.duration 
          })
        });

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        // 注意：生产环境需处理跨域和路径前缀
        this.videoUrl = `http://localhost:8000${data.video_url}`;
      } catch (err) {
        this.error = err.message || 'Failed to generate video';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f8fafc; }
#app { max-width: 800px; margin: 0 auto; padding: 2rem; }
header { text-align: center; margin-bottom: 2rem; }
header h1 { font-size: 2.5rem; color: #0f172a; margin-bottom: 0.5rem; }
header p { color: #64748b; }

.container { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
textarea { width: 100%; padding: 1rem; margin-bottom: 1rem; border: 1px solid #cbd5e1; border-radius: 8px; resize: vertical; }
.controls { display: flex; gap: 1rem; margin-bottom: 1rem; }
.controls input { flex: 1; padding: 0.75rem; border: 1px solid #cbd5e1; border-radius: 8px; }
.controls button { 
  background: #3b82f6; color: white; border: none; padding: 0.75rem 1.5rem; 
  border-radius: 8px; cursor: pointer; font-weight: 600;
}
.controls button:disabled { opacity: 0.7; cursor: not-allowed; }

.error { color: #ef4444; margin-bottom: 1rem; padding: 0.5rem; background: #fee; border-radius: 4px; }
.result video { width: 100%; border-radius: 8px; margin: 1rem 0; }
.result a { display: inline-block; margin-top: 0.5rem; color: #3b82f6; text-decoration: none; }
</style>