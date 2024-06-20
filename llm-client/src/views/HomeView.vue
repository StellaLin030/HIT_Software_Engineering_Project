<template>
  <div class="home">
    <!-- 顶部栏 -->
    <div class="top-bar">
      <div class="left">
        <span>ChatWithAIs V1 | 一站式大语言模型访问平台</span>
      </div>
      <div class="right">
        <router-link to="/login" class="home-link">登录</router-link>
        <router-link to="/register" class="home-link">注册</router-link>
      </div>
    </div>
    <!-- 轮播图片 -->
    <div class="carousel">
      <div class="carousel-item" v-for="(image, index) in images" :key="index" :class="{ active: currentIndex === index }">
        <img :src="image.src" :alt="image.alt">
        <div class="carousel-caption" :style="{color: index === 2 ? 'black': 'white'}" v-html="image.caption"></div>
      </div>
      <button class="prev" @click="prevSlide">&#10094;</button>
      <button class="next" @click="nextSlide">&#10095;</button>
    </div>
    <!-- 指示点 -->
    <div class="dots">
      <span v-for="(image, index) in images" :key="index" :class="{ active: currentIndex === index }" @click="goToSlide(index)"></span>
    </div>
    <!-- 页面内容 -->
    <!--<h2>不知道说什么，没有审美，改不出来好看的页面 :(</h2>-->
    <div class="sec-notice"><br>©2024 Created by HIT-ChatWithAIs team</div>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      images: [
        { src: require('../assets/homepage1.png'), alt: 'homepage1', caption: '打造多大语言模型集成的智能助手平台，<br>为用户提供一站式信息查询服务。' },
        { src: require('../assets/homepage2.png'), alt: 'homepage2', caption: '实现一站式大语言模型访问，<br>支持ChatGPT、文心一言、通义千问。' },
        { src: require('../assets/homepage3.png'), alt: 'homepage3', caption: '关注系统的长期运行和维护，<br>确保系统为用户提供稳定、优质的服务。' },
      ],
      currentIndex: 0,
      intervalId: null,
    };
  },
  mounted() {
    this.startCarousel();
  },
  methods: {
    startCarousel() {
      this.intervalId = setInterval(() => {
        this.nextSlide();
      }, 5000);
    },
    nextSlide() {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
    },
    prevSlide() {
      this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
    },
    goToSlide(index) {
      this.currentIndex = index;
    }
  },
  beforeDestroy() {
    clearInterval(this.intervalId);
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}

.home {
  text-align: center;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #D6EAF8;
  padding: 10px;
  color: #1296db;
  height: 35px;
  font-weight: bold;
}

.top-bar .left {
  font-size: 20px;
}

.top-bar .right .home-link {
  margin-left: 15px;
  padding: 8px 16px;
  background-color: #ffffff;
  color: #1296db;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s, color 0.3s;
  font-weight: bold;
}

.top-bar .right .home-link:hover {
  background-color: #1296db;
  color: #ffffff;
}

.carousel {
  position: relative;
  margin-top: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 720px; /* 设置轮播图容器高度 */
  width: 1280px; /* 设置轮播图容器宽度 */
  margin: 0 auto; /* 使轮播图居中 */
  overflow: hidden; /* 隐藏溢出的部分 */
}

.carousel-item {
  position: absolute;
  opacity: 0;
  transition: opacity 0.5s ease;
  width: 100%;
  height: 100%;
}

.carousel-item.active {
  opacity: 1;
  position: absolute;
}

.carousel img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持图片比例并覆盖整个容器 */
  border-radius: 10px;
}

.carousel-caption {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: black; /* 默认文本颜色 */
  font-size: 35px; /* 增大字体大小 */
  text-align: center; /* 文本居中对齐 */
  background-color: transparent; /* 移除背景 */
  font-weight: 550;
}

.carousel .carousel-item.active .carousel-caption {
  color: white; /* 对于活动幻灯片，更改文本颜色为白色 */
}


.prev, .next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  font-size: 18px;
  border-radius: 15%;
}

.prev {
  left: 10px;
}

.next {
  right: 10px;
}

.dots {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.dots span {
  height: 10px;
  width: 10px;
  margin: 0 5px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
  cursor: pointer;
}

.dots span.active {
  background-color: #717171;
}

.home h2 {
  margin-top: 20px;
  font-size: 18px;
}

.sec-notice {
  height: 3.5%;
  font-size: 12px;
  font-family: Söhne, ui-sans-serif;
  color: rgb(155, 155, 155);
  display: flex;
  justify-content: center;
}
</style>
