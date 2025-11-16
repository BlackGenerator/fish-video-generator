<!-- src/App.vue -->
<template>
  <div id="app">
    <header>
      <div class="container">
        <div class="header-content">
          <div class="logo">
            <i class="fas fa-microphone-alt"></i> 文字转视频
          </div>
          <nav>
            <ul class="nav-links">
              <li><a href="#home">首页</a></li>
              <li><a href="#features">功能</a></li>
              <li><a href="#about">关于</a></li>
              <li><a href="#contact">联系</a></li>
            </ul>
          </nav>
        </div>
      </div>
    </header>

    <section class="hero" id="home">
      <div class="container">
        <h1 class="animate__animated animate__fadeInDown">创作您的专属视频</h1>
        <p class="animate__animated animate__fadeInUp">从文字到图片，从声音到视频，一站式内容创作平台</p>
        
        <div class="process-steps">
          <div class="step" data-aos="fade-up" data-aos-delay="100">
            <div class="step-number">1</div>
            <h3>输入文字</h3>
            <p>撰写您的脚本内容</p>
          </div>
          <div class="step" data-aos="fade-up" data-aos-delay="200">
            <div class="step-number">2</div>
            <h3>添加视觉</h3>
            <p>上传或生成配图</p>
          </div>
          <div class="step" data-aos="fade-up" data-aos-delay="300">
            <div class="step-number">3</div>
            <h3>克隆声音</h3>
            <p>定制个性化语音</p>
          </div>
          <div class="step" data-aos="fade-up" data-aos-delay="400">
            <div class="step-number">4</div>
            <h3>生成视频</h3>
            <p>输出完整作品</p>
          </div>
        </div>
      </div>
    </section>

    <main class="main-content">
      <div class="container">
        <div class="content-grid">
          <div class="card" data-aos="fade-right">
            <h2><i class="fas fa-font"></i> 文字输入</h2>
            <textarea 
              class="text-input" 
              placeholder="请输入您想要转换为语音的文字内容..."
              v-model="textContent"
            ></textarea>
            <div class="form-group">
              <label for="voiceStyle">语音风格</label>
              <select id="voiceStyle" class="form-control" v-model="voiceStyle">
                <option value="neutral">中性</option>
                <option value="warm">温暖</option>
                <option value="professional">专业</option>
                <option value="energetic">活力</option>
              </select>
            </div>
            <button class="btn" @click="processText">
              <i class="fas fa-paper-plane"></i> 处理文字
            </button>
            <div :class="['status-badge', `status-${textStatus.status}`]">
              {{ textStatus.message }}
            </div>
          </div>

          <div class="card" data-aos="fade-left">
            <h2><i class="fas fa-image"></i> 图片处理</h2>
            <div class="file-upload" @click="$refs.imageUpload.click()">
              <input 
                type="file" 
                ref="imageUpload"
                accept="image/*" 
                @change="uploadImage"
                style="display: none;"
              >
              <i class="fas fa-cloud-upload-alt" style="font-size: 3rem; color: var(--primary); margin-bottom: 1rem;"></i>
              <p>点击上传图片</p>
              <small>或将图片拖拽到这里</small>
              
              <img v-if="uploadedImage" :src="uploadedImage" class="uploaded-image" alt="Uploaded">
            </div>
            
            <div class="form-group">
              <label for="imageStyle">图片风格</label>
              <select id="imageStyle" class="form-control" v-model="imageStyle">
                <option value="original">原图</option>
                <option value="cartoon">卡通</option>
                <option value="sketch">素描</option>
                <option value="watercolor">水彩</option>
              </select>
            </div>
            <button class="btn" @click="generateImage" style="margin-right: 1rem;">
              <i class="fas fa-magic"></i> 风格转换
            </button>
            <button class="btn btn-secondary" @click="removeImage">
              <i class="fas fa-trash"></i> 移除图片
            </button>
            <div :class="['status-badge', `status-${imageStatus.status}`]">
              {{ imageStatus.message }}
            </div>
          </div>

          <div class="card" data-aos="fade-right">
            <h2><i class="fas fa-microphone-alt"></i> 语音克隆</h2>
            <div class="form-group">
              <label for="sampleAudio">声音样本</label>
              <div class="file-upload" @click="$refs.sampleAudio.click()">
                <input 
                  type="file" 
                  ref="sampleAudio"
                  id="sampleAudio"
                  accept="audio/*"
                  style="display: none;"
                >
                <p>上传声音样本音频</p>
                <small>(支持mp3/wav格式)</small>
              </div>
            </div>
            <div class="form-group">
              <label for="pitch">音调调节</label>
              <input type="range" id="pitch" min="-2" max="2" value="0" class="form-control" v-model="pitch">
            </div>
            <button class="btn" @click="cloneVoice">
              <i class="fas fa-clone"></i> 克隆声音
            </button>
            <div :class="['status-badge', `status-${voiceStatus.status}`]">
              {{ voiceStatus.message }}
            </div>
          </div>

          <div class="card" data-aos="fade-left">
            <h2><i class="fas fa-video"></i> 视频生成</h2>
            <div class="form-group">
              <label for="duration">视频时长</label>
              <select id="duration" class="form-control" v-model="duration">
                <option value="10">10分钟</option>
                <option value="15">15分钟</option>
                <option value="20">20分钟</option>
                <option value="custom">自定义</option>
              </select>
            </div>
            <div class="form-group" v-show="duration === 'custom'">
              <label>自定义时长 (秒):</label>
              <input type="number" id="customSeconds" min="1" max="7200" v-model="customSeconds">
            </div>
            <button class="btn" @click="generateVideo" style="width: 100%;">
              <i class="fas fa-play"></i> 生成视频
            </button>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: videoProgress + '%' }"></div>
            </div>
            <div :class="['status-badge', `status-${videoStatus.status}`]">
              {{ videoStatus.message }}
            </div>
            <div style="margin-top: 1rem;">
              <span class="status-badge status-processing">处理中...</span>
              <span class="status-badge status-completed">已完成</span>
            </div>
          </div>

          <div class="card video-preview" data-aos="fade-up">
            <h2><i class="fas fa-eye"></i> 视频预览</h2>
            <p>您的最终视频将在下方显示</p>
            <video v-if="finalVideo" :src="finalVideo" controls class="final-video"></video>
            <button class="btn btn-secondary" @click="downloadVideo" style="margin-right: 1rem;">
              <i class="fas fa-download"></i> 下载视频
            </button>
            <button class="btn" @click="shareVideo">
              <i class="fas fa-share"></i> 分享视频
            </button>
          </div>
        </div>
      </div>
    </main>

    <footer class="footer">
      <div class="container">
        <p>&copy; 2024 文字转视频创作平台. 用技术赋能创意表达.</p>
        <p>联系我们: <a href="mailto:contact@example.com">contact@example.com</a></p>
      </div>
    </footer>

    <!-- Processing Modal -->
    <div id="processingModal" class="modal" v-show="showModal">
      <div class="modal-content">
        <span class="close-modal" @click="hideProcessingModal">&times;</span>
        <h2>处理进度</h2>
        <div class="progress-bar" style="margin: 1rem 0;">
          <div class="progress-fill" :style="{ width: modalProgress + '%' }"></div>
        </div>
        <p>{{ modalMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      // Text section
      textContent: '',
      voiceStyle: 'neutral',
      textStatus: { status: 'processing', message: '待处理' },
      
      // Image section
      uploadedImage: null,
      imageStyle: 'original',
      imageStatus: { status: 'processing', message: '待处理' },
      
      // Voice section
      pitch: 0,
      voiceStatus: { status: 'processing', message: '待处理' },
      
      // Video section
      duration: '10',
      customSeconds: 600,
      videoProgress: 0,
      videoStatus: { status: 'processing', message: '待处理' },
      finalVideo: null,
      
      // Modal
      showModal: false,
      modalProgress: 0,
      modalMessage: '正在处理您的请求...',
      
      // API config
      API_CONFIG: {
        IMAGE_GEN_URL: '/generate',
        VIDEO_GEN_URL: '/generate'
      }
    };
  },
  methods: {
    async processText() {
      if (!this.textContent.trim()) {
        alert('请输入文字内容');
        return;
      }
      
      this.showProcessingModal('正在处理文字...');
      this.textStatus = { status: 'processing', message: '处理中...' };
      
      // Simulate processing
      setTimeout(() => {
        this.textStatus = { status: 'completed', message: '处理完成' };
        this.hideProcessingModal();
      }, 2000);
    },
    
    uploadImage(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      this.showProcessingModal('正在处理图片...');
      this.imageStatus = { status: 'processing', message: '上传中...' };
      
      const reader = new FileReader();
      reader.onload = (e) => {
        this.uploadedImage = e.target.result;
        this.imageStatus = { status: 'completed', message: '上传完成' };
        this.hideProcessingModal();
      };
      reader.readAsDataURL(file);
    },
    
    async generateImage() {
      if (!this.textContent.trim()) {
        alert('请先输入文字内容以生成图片');
        return;
      }
      
      this.showProcessingModal('正在生成图片...');
      this.imageStatus = { status: 'processing', message: '生成中...' };
      
      try {
        // In a real app, you would call the API here
        // const response = await axios.post(this.API_CONFIG.IMAGE_GEN_URL, { text: this.textContent });
        // this.uploadedImage = response.data.imageUrl;
        
        // For demo purposes, we'll just simulate it
        setTimeout(() => {
          this.imageStatus = { status: 'completed', message: '图片生成完成' };
          this.hideProcessingModal();
        }, 2000);
      } catch (error) {
        this.imageStatus = { status: 'error', message: '生成失败: ' + error.message };
        this.hideProcessingModal();
        alert('图片生成失败: ' + error.message);
      }
    },
    
    removeImage() {
      this.uploadedImage = null;
      this.imageStatus = { status: 'processing', message: '待处理' };
    },
    
    cloneVoice() {
      this.showProcessingModal('正在克隆声音...');
      this.voiceStatus = { status: 'processing', message: '处理中...' };
      
      setTimeout(() => {
        this.voiceStatus = { status: 'completed', message: '声音克隆完成' };
        this.hideProcessingModal();
      }, 2000);
    },
    
    async generateVideo() {
      if (!this.textContent.trim()) {
        alert('请先输入文字内容');
        return;
      }
      
      const totalSeconds = this.duration === 'custom' ? 
        parseInt(this.customSeconds) : 
        parseInt(this.duration) * 60;
      
      this.showProcessingModal(`正在生成${totalSeconds}秒视频...`);
      this.videoStatus = { status: 'processing', message: '生成中...' };
      
      try {
        // In a real app, you would call the API here
        // const response = await axios.post(this.API_CONFIG.VIDEO_GEN_URL, {
        //   text: this.textContent,
        //   duration: totalSeconds,
        //   imageUrl: this.uploadedImage,
        //   voiceStyle: this.voiceStyle
        // });
        // this.finalVideo = response.data.videoUrl;
        
        // For demo purposes, we'll just simulate it
        this.simulateVideoGeneration(totalSeconds);
      } catch (error) {
        this.videoStatus = { status: 'error', message: '生成失败: ' + error.message };
        this.hideProcessingModal();
        alert('视频生成失败: ' + error.message);
      }
    },
    
    simulateVideoGeneration(seconds) {
      let progress = 0;
      const interval = setInterval(() => {
        progress += 5;
        this.videoProgress = progress;
        this.modalProgress = progress;
        
        if (progress >= 100) {
          clearInterval(interval);
          this.videoStatus = { status: 'completed', message: '视频生成完成' };
          this.finalVideo = 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'; // Demo video
          this.hideProcessingModal();
        }
      }, seconds * 50); // Adjust timing based on requested duration
    },
    
    downloadVideo() {
      if (!this.finalVideo) {
        alert('视频尚未生成');
        return;
      }
      
      const link = document.createElement('a');
      link.href = this.finalVideo;
      link.download = 'output_video.mp4';
      link.click();
    },
    
    shareVideo() {
      if (!this.finalVideo) {
        alert('视频尚未生成');
        return;
      }
      
      if (navigator.share) {
        navigator.share({
          title: '我的创作视频',
          text: '这是我用文字转视频平台创作的作品',
          url: this.finalVideo
        });
      } else {
        alert('分享功能不支持，您可以手动下载后分享');
      }
    },
    
    showProcessingModal(message) {
      this.modalMessage = message;
      this.modalProgress = 0;
      this.showModal = true;
    },
    
    hideProcessingModal() {
      this.showModal = false;
    }
  }
};
</script>

<style>
:root {
  --bg: #F8FAFC;
  --primary: #2563EB;
  --secondary: #64748B;
  --accent: #F59E0B;
  --card: #FFFFFF;
  --shadow: rgba(37, 99, 235, 0.1);
  --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: var(--bg);
  color: var(--secondary);
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

header {
  background: var(--card);
  box-shadow: 0 2px 10px var(--shadow);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
}

.nav-links {
  display: flex;
  gap: 2rem;
  list-style: none;
}

.nav-links a {
  text-decoration: none;
  color: var(--secondary);
  font-weight: 500;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: var(--primary);
}

.hero {
  text-align: center;
  padding: 4rem 0;
  background: var(--gradient);
  color: white;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.process-steps {
  display: flex;
  justify-content: space-around;
  margin: 3rem 0;
  flex-wrap: wrap;
  gap: 2rem;
}

.step {
  text-align: center;
  flex: 1;
  min-width: 200px;
}

.step-number {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 auto 1rem;
}

.step h3 {
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.main-content {
  padding: 4rem 0;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.card {
  background: var(--card);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px var(--shadow);
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px var(--shadow);
}

.card h2 {
  color: var(--primary);
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.text-input {
  width: 100%;
  min-height: 150px;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-family: inherit;
  resize: vertical;
  margin-bottom: 1rem;
  transition: border-color 0.3s;
}

.text-input:focus {
  outline: none;
  border-color: var(--primary);
}

.file-upload {
  border: 2px dashed #e2e8f0;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: border-color 0.3s, background 0.3s;
}

.file-upload:hover {
  border-color: var(--primary);
  background: #f1f5f9;
}

.uploaded-image {
  max-width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.btn {
  background: var(--primary);
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
}

.btn-secondary {
  background: transparent;
  color: var(--primary);
  border: 2px solid var(--primary);
}

.btn-secondary:hover {
  background: var(--primary);
  color: white;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin: 1rem 0;
}

.progress-fill {
  height: 100%;
  background: var(--primary);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  margin-bottom: 1rem;
  font-weight: 600;
}

.video-preview {
  grid-column: 1 / -1;
  text-align: center;
}

.final-video {
  width: 100%;
  max-width: 600px;
  height: 338px;
  object-fit: cover;
  border-radius: 12px;
  margin-top: 1rem;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  margin: 0.5rem;
}

.status-processing {
  background: #fef3c7;
  color: #92400e;
}

.status-completed {
  background: #dcfce7;
  color: #166534;
}

.footer {
  background: var(--card);
  padding: 3rem 0;
  text-align: center;
  margin-top: 4rem;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }
  
  .process-steps {
    flex-direction: column;
    align-items: center;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .nav-links {
    display: none;
  }
}

.modal {
  display: none;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
}

.modal-content {
  background: var(--card);
  margin: 5% auto;
  padding: 2rem;
  border-radius: 12px;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.close-modal {
  float: right;
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
  color: var(--secondary);
}

.close-modal:hover {
  color: var(--primary);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--primary);
}

.form-control {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>