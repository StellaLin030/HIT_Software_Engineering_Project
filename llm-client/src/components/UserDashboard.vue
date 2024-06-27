<template>

  <div class="home">
    <div class="home-right">

      <div class="right-version">
        <div class="llm-chat-demo">
          <span class="chat-demo">ChatWIthAIs</span><span class="version"> V1</span>
        </div>

        <!-- 添加登出和反馈按钮 -->
        <div class="user-actions">
          <button @click="goToLogout" class="action-button logout-button">登出</button>
          <button @click="goToFeedback" class="action-button feedback-button">反馈</button>
        </div>
      </div>

      <div class="right-body" :class="wenxin_messages.length === 0 ? 'nodata' : ''" ref="messageContainer">
        <div class="container">
          <div class="left">
            <div v-for="(message, index) in wenxin_messages" class="main-message" :key="index"
                 :class="{'user-message': message.sender === 'user', 'friend-message': message.sender === 'friend'}">
              <!-- 显示用户标识和图片 -->
              <div class="message-sender"
                   :class="{'user-message': message.sender === 'user', 'friend-message': message.sender === 'friend'}">
                <img v-if="message.sender === 'user'" src="@/assets/我的.png" alt="User Icon">
                <img v-else-if="message.sender === 'friend'" src="@/assets/文心一言.png" alt="Friend Icon">
                <span class="message-sender-name"
                      :class="message.sender === 'user' ? 'user-color' : 'friend-color'">{{ message.sender }}:</span>
              </div>
              <div v-if="message.sender === 'user'" class="user-message">{{ message.content }}</div>
              <div v-else class="friend-message" v-html="message.content"></div>
            </div>
          </div>
          <div class="mid">
            <div v-for="(message, index) in tongyi_messages" class="main-message" :key="index"
                 :class="{'user-message': message.sender === 'user', 'friend-message': message.sender === 'friend'}">
              <!-- 显示用户标识和图片 -->
              <div class="message-sender"
                   :class="{'user-message': message.sender === 'user', 'friend-message': message.sender === 'friend'}">
                <img v-if="message.sender === 'user'" src="@/assets/我的.png" alt="User Icon">
                <img v-else-if="message.sender === 'friend'" src="@/assets/通义千问.png" alt="Friend Icon">
                <span class="message-sender-name"
                      :class="message.sender === 'user' ? 'user-color' : 'friend-color'">{{ message.sender }}:</span>
              </div>
              <div v-if="message.sender === 'user'" class="user-message">{{ message.content }}</div>
              <div v-else class="friend-message" v-html="message.content"></div>
            </div>
          </div>
          <div class="right">
            <div v-for="(message, index) in chatgpt_messages" class="main-message" :key="index"
                 :class="{'user-message': message.sender === 'user', 'friend-message': message.sender === 'friend'}">
              <!-- 显示用户标识和图片 -->
              <div class="message-sender"
                   :class="{'user-message': message.sender === 'user', 'friend-message': message.sender === 'friend'}">
                <img v-if="message.sender === 'user'" src="@/assets/我的.png" alt="User Icon">
                <img v-else-if="message.sender === 'friend'" src="@/assets/chatgpt.png" alt="Friend Icon">
                <span class="message-sender-name"
                      :class="message.sender === 'user' ? 'user-color' : 'friend-color'">{{ message.sender }}:</span>
              </div>
              <div v-if="message.sender === 'user'" class="user-message">{{ message.content }}</div>
              <div v-else class="friend-message" v-html="message.content"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="right-input" @keyup.enter="handleSearch">
        <!-- 输入框 -->
        <el-input v-model="queryKeyword" placeholder="给Chat Demo发送消息" class="input"></el-input>
        <!-- 查询按钮 -->
        <el-button v-if="!loading" type="primary" @click="handleSearch">
          <img  class="up-load" src="@/assets/上传.png">
        </el-button>
        <el-button v-if="loading" type="primary" @click="closeEventSource">
          <img  class="up-load" src="@/assets/等待.png" >
        </el-button>
      </div>

      <div class="sec-notice">Chat Demo may also make mistakes. Please consider checking important information.</div>
    </div>
  </div>
</template>

<script>
import MarkdownIt from 'markdown-it';
import markdownItFootnote from 'markdown-it-footnote';
import markdownItTaskLists from 'markdown-it-task-lists';
import markdownItAbbr from 'markdown-it-abbr';
import markdownItContainer from 'markdown-it-container';
import hljs from 'highlight.js';
import markdownItHighlightjs from 'markdown-it-highlightjs';
import router from '../router';

export default {
  name: 'UserDashboard',
  components: {},
  computed: {
    // 将 Markdown 文本渲染为 HTML
    html() {
      return this.md.render(this.message);
    }
  },
  data() {
    return {
      md: new MarkdownIt()
          .use(markdownItFootnote)
          .use(markdownItTaskLists, {enabled: true})
          .use(markdownItAbbr)
          .use(markdownItContainer, 'warning')
          .use(markdownItHighlightjs, {hljs}), // 添加 markdown-it-highlightjs 插件
      queryKeyword: '',
      tempResult: {},
      loading: false,
      wenxin_messages: [],
      tongyi_messages:[],
      chatgpt_messages:[],
      socket: null,
      eventSource: null, // 添加事件源变量
      stopIcon: '@/assets/等待.png',
      uploadIcon: '@/assets/上传.png'
    }
  },
  methods: {
    async handleSearch() {
      // 如果正在加载中，则不执行新的搜索操作
      if (this.loading) {
        return;
      }

      const keyword = this.queryKeyword;
      this.loading = true;
      try {
        let zxakey = "zxa";
        // 初始化一个用于 SSE 的 message 对象
        let wenxin_sseMessage = {
          orgcontent: '',
          content: '',
          sender: 'friend',
          zxakey: zxakey
        };
        let tongyi_sseMessage = {
          orgcontent: '',
          content: '',
          sender: 'friend',
          zxakey: zxakey
        };
        let chatgpt_sseMessage = {
          orgcontent: '',
          content: '',
          sender: 'friend',
          zxakey: zxakey
        };

        this.wenxin_messages.push({
          content: keyword,
          sender: 'user'
        });
        this.tongyi_messages.push({
          content: keyword,
          sender: 'user'
        });
        this.chatgpt_messages.push({
          content: keyword,
          sender: 'user'
        });

        this.$nextTick(() => {
          this.scrollToBottom();
        });

        let wenxin_friendMessage = wenxin_sseMessage;
        // 创建一个新的 EventSource 实例
        this.wenxin_eventSource = new EventSource('/api/wenxin?query=' + keyword);
        // 设置消息事件监听器
        this.wenxin_eventSource.onmessage = (event) => {
          try {
            const dataObject = JSON.parse(event.data);
            // 判断是否为最后一个消息，如果是，则关闭事件源
            if (dataObject.message === 'done') {
              this.wenxin_eventSource.close();
              this.loading = false;
            }
            if (dataObject.message != 'done') {
              // 累加接收到的数据到 friendMessage.orgcontent 中
              wenxin_friendMessage.orgcontent += dataObject.message.toLocaleString();
              wenxin_friendMessage.orgcontent = wenxin_friendMessage.orgcontent.replace(/\*\*\s*([^*]*?)\s*(:\s*)?\*\*/g, '**$1$2**');
              // 更新 friendMessage.content，这里假设 md.render 可以处理累加的字符串
              wenxin_friendMessage.content = this.md.render(wenxin_friendMessage.orgcontent);
            }
            this.scrollToBottom();
          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        };
        this.wenxin_messages.push(wenxin_sseMessage);
        this.queryKeyword = ''; // 清空输入框
        this.wenxin_eventSource.onerror = error => {
          console.error('EventSource failed:', error);
          this.wenxin_eventSource.close();
        };
        let tongyi_friendMessage = tongyi_sseMessage;
        // 创建一个新的 EventSource 实例
        this.tongyi_eventSource = new EventSource('/api/tongyi?query=' + keyword);
        // 设置消息事件监听器
        this.tongyi_eventSource.onmessage = (event) => {
          try {
            const dataObject = JSON.parse(event.data);
            // 判断是否为最后一个消息，如果是，则关闭事件源
            if (dataObject.message === 'done') {
              this.tongyi_eventSource.close();
              this.loading = false;
            }
            if (dataObject.message != 'done') {
              // 累加接收到的数据到 friendMessage.orgcontent 中
              tongyi_friendMessage.orgcontent += dataObject.message.toLocaleString();
              tongyi_friendMessage.orgcontent = tongyi_friendMessage.orgcontent.replace(/\*\*\s*([^*]*?)\s*(:\s*)?\*\*/g, '**$1$2**');
              // 更新 friendMessage.content，这里假设 md.render 可以处理累加的字符串
              tongyi_friendMessage.content = this.md.render(tongyi_friendMessage.orgcontent);
            }
            this.scrollToBottom();
          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        };
        this.tongyi_messages.push(tongyi_sseMessage);
        this.queryKeyword = ''; // 清空输入框
        this.tongyi_eventSource.onerror = error => {
          console.error('EventSource failed:', error);
          this.tongyi_eventSource.close();
        };
        let chatgpt_friendMessage = chatgpt_sseMessage;
        // 创建一个新的 EventSource 实例
        this.chatgpt_eventSource = new EventSource('/api/chatgpt?query=' + keyword);
        // 设置消息事件监听器
        this.chatgpt_eventSource.onmessage = (event) => {
          try {
            const dataObject = JSON.parse(event.data);
            // 判断是否为最后一个消息，如果是，则关闭事件源
            if (dataObject.message === 'done') {
              this.chatgpt_eventSource.close();
              this.loading = false;
            }
            if (dataObject.message != 'done') {
              // 累加接收到的数据到 friendMessage.orgcontent 中
              chatgpt_friendMessage.orgcontent += dataObject.message.toLocaleString();
              chatgpt_friendMessage.orgcontent = chatgpt_friendMessage.orgcontent.replace(/\*\*\s*([^*]*?)\s*(:\s*)?\*\*/g, '**$1$2**');
              // 更新 friendMessage.content，这里假设 md.render 可以处理累加的字符串
              chatgpt_friendMessage.content = this.md.render(chatgpt_friendMessage.orgcontent);
            }
            this.scrollToBottom();
          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        };
        this.chatgpt_messages.push(chatgpt_sseMessage);
        this.queryKeyword = ''; // 清空输入框
        this.chatgpt_eventSource.onerror = error => {
          console.error('EventSource failed:', error);
          this.chatgpt_eventSource.close();
        };

      } catch (error) {
        console.error('发送消息时出错：', error);
      } finally {
      }
    },
    closeEventSource() {
      this.loading = false;
      if (this.eventSource) {
        this.eventSource.close();
      }
    },
    scrollToBottom() {
      const messageContainer = this.$refs.messageContainer;
      if (messageContainer) {
        messageContainer.scrollTop = messageContainer.scrollHeight;
      }
    },
    beforeDestroy() {
      if (this.eventSource) {
        this.eventSource.close();
      }
    },
    goToLogout() {
      router.push({ name: 'Logout' });
    },
    goToFeedback(){
      router.push({ name: 'Feedback'});
    }
  },
}
</script>

<style scoped>
.home {
  height: 100%;
  display: flex;
}

.home-right {
  width: 100%;
}

.right-version {
//width: 60%;
  margin: auto;
//background-color: #F9FFD8;
  height: 5%;
  display: flex;
  justify-content: start;
  align-items: center;
  border-radius: 15px;
  margin-bottom: 12px;
}

.version {
  color: rgb(155, 155, 155);
}

.llm-chat-demo {
  width: 58%;
  margin: auto;
//margin-left: 20px;
//font-family: "黑体", "SimHei", sans-serif;
  font-family: Söhne, ui-sans-serif, system;
  font-variation-settings: normal;
  font-weight: 550;
  font-size: 20px;
  cursor: pointer;
  color-scheme: light;
}

.chat-demo {
  opacity: 0.65; /* 设置透明度为 0.7，您可以根据需要调整这个值 */
}

.right-body {
  height: 85%;
  overflow-y: auto;
}

.user-color {
  color: #1296db;
}

.friend-color {
  color: #77FC5D;
}
.nodata {
  background-image: url("@/assets/happy.png");
  background-repeat: no-repeat;
  background-size: 35%;
  background-position: center 50%;
}

.main-message {
  margin: auto;
  width: 90%;
  justify-content: center;
}

.message-sender-name {
  margin-left: 10px;
//font-family: "黑体", "SimHei", sans-serif;
  font-family: Söhne, ui-sans-serif, system;
  font-weight: 550;
  font-size: 18px;
}

.right-input {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 6.5%;

  position: relative;
}

.sec-notice {
  height: 3.5%;
  font-size: 12px;
  font-family: Söhne, ui-sans-serif;
  color: rgb(155, 155, 155);
  display: flex;
  justify-content: center;
}

.input {
  width: 58%;
  margin-right: 5px;
}

.up-load {
//width: 30px;
}

::v-deep .el-button {
  padding: 5px 6px;
}

::v-deep .el-input__inner {
  height: 52px;
  border-radius: 15px;
  border: 1px solid #DCDFE6;
}

::v-deep .el-button--primary {
  position: relative;
  right: 3.5%;
  background-color: rgba(180, 180, 180, 0.3) !important;
  color: black !important;
  border-color: rgba(180, 180, 180, 0.3) !important;
}

.user-message {
  text-align: left;
  padding: 5px;
  margin-bottom: 5px;
  border-radius: 15px;

}

.friend-message {
  background-color: rgba(227, 255, 255, 0.2); /* 这里的 0.5 是透明度，你可以根据需要调整 */
  text-align: left;
  padding: 5px;
  margin-bottom: 5px;
}

.container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr; /* 三列等宽 */
    gap: 10px; /* 列间距 */
    height: 100vh; /* 设定高度以便示范 */
}

.left, .mid, .right {
  border: 1px solid #ccc; /* 边框以便示范 */
  padding: 10px;
  overflow: auto; /* 内容溢出时显示滚动条 */
  box-sizing: border-box; /* 包括padding和border在内的宽度计算 */
}

.left {
  grid-column: 1 / 2;
  min-width: 200px; /* 最小宽度 */
}

.mid {
  grid-column: 2 / 3;
  min-width: 200px; /* 最小宽度 */
}

.right {
  grid-column: 3 / 4;
  min-width: 200px; /* 最小宽度 */
}
.logout-button,
.feedback-button {
  background-color: #1296db;
  color: #fff;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-right: 10px;
}

.logout-button:hover,
.feedback-button:hover {
  background-color: #0056b3;
}

.user-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  position: absolute;
  top: 10px; /* 向下移动 */
  right: 10px;
}


::v-deep .friend-message pre .hljs {
  border-radius: 10px !important; /* 圆角 */
  background-color: #FAF7F7; /* 例子中的背景色 */
}

/* 设置滚动条的样式 */
::-webkit-scrollbar {
  width: 6px; /* 设置滚动条宽度 */
}

/* 设置滚动条轨道的样式 */
::-webkit-scrollbar-track {
  background: #f1f1f1; /* 设置滚动条轨道的背景色 */
}

/* 设置滚动条滑块的样式 */
::-webkit-scrollbar-thumb {
  background: #888; /* 设置滚动条滑块的背景色 */
  border-radius: 3px; /* 设置滚动条滑块的圆角 */
}

/* 鼠标悬停时滚动条滑块的样式 */
::-webkit-scrollbar-thumb:hover {
  background: #555; /* 设置鼠标悬停时滚动条滑块的背景色 */
}
</style>

