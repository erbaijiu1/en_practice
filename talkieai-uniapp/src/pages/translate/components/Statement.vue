<template>
  <view class="statement-container">
    <view class="chat-list-box">
      <view class="chat-list-left-box">
        <view class="chat-list-left-top">
          <view class="selectable-text" selectable @mouseup="handleTextTouch"   @touchend="handleTextTouch"
          @longpress="handleWordLongPress"
          >
            {{ collect.en }} 
          </view>
        </view>
      </view>

      <view class="chat-list-action-box">
        <AudioPlayer class="chat-list-action_playing btn-box" :messageId="collect.message_id"
          :content="collect.en" />
        <!-- <image v-if="!cannotCancel" @tap="handleDelete" class="chat-list-action btn-box" src="/static/deleted.png" mode="heightFix" /> -->
      </view>
    </view>
    <view class="chat-list-left-bot">
      <text>{{ collect.cn }}</text>
    </view>

  </view>
  <WordAnalysisPopup ref="wordAnalysisPopup" />

</template>

<script setup lang="ts">
import { ref, defineEmits, defineProps } from "vue";
import AudioPlayer from "@/components/AudioPlayer.vue";
import type { PracticeSentence } from "@/models/models";
import type { TranslateExample } from "@/models/models";
import accountRequest from "@/api/account";
import WordAnalysisPopup from "@/components/WordAnalysisPopup.vue";
import { nextTick } from 'vue';

// 添加选中功能
const wordAnalysisPopup = ref(null);

const handleWordLongPress = (e: any) => {
  console.log("handleWordLongPress: ", e);
  const selectedText = e.detail.text?.trim();
  if (selectedText) {
    wordAnalysisPopup.value.open(selectedText);
  }
};

const handleTextTouch = () => {
  const platform = uni.getSystemInfoSync().platform.toLowerCase();
  console.log("platform:", platform);
    // 明确列出支持 DOM 操作的平台
    const supportedDOMPlatforms = [
    // 'devtools',     // H5 开发者工具
    'h5',           // H5 页面
    'app-plus',     // App（H5+）
    'mp-qq',        // QQ 小程序
    'mp-baidu',     // 百度小程序
    'mp-toutiao'    // 头条小程序
  ];

  if (!supportedDOMPlatforms.includes(platform)) {
    // 不在白名单内的平台（如微信小程序），直接返回
    return;
  }

  // 只有在非小程序平台才执行 DOM 操作
  const handleSelection = () => {
    const selection = window.getSelection();
    if (!selection || selection.rangeCount === 0) return;

    const selectedText = selection.toString().trim();
    if (selectedText) {
      wordAnalysisPopup.value.open(selectedText);
    }

    document.removeEventListener('mouseup', handleSelection);
  };

  document.addEventListener('mouseup', handleSelection);
};



const emit = defineEmits();
// 定义Collect类型为prop
const props = defineProps<{
  collect: TranslateExample;
  cannotCancel?: boolean;
}>();

const handleDelete = () => {
  // 调用提示用户是否删除
  uni.showModal({
    title: "提示",
    content: "是否删除该收藏",
    confirmColor: "#6236ff",
    success: (res) => {
      if (res.confirm) {
        // 用户点击确定
        accountRequest
          .cancelCollect({
            type: props.collect.type,
            message_id: props.collect.message_id,
            content: props.collect.en,
          })
          .then(() => {
            // 需要父组件重新刷新数据
            uni.showToast({
              title: "删除成功",
              icon: "none",
            });
            // 触发父组件的事件
            emit("deleteCollect", props.collect);
          });
      } else if (res.cancel) {
        // 用户点击取消
      }
    },
  });
};
</script>

<style lang="less">
.statement-container {
  // padding: 32rpx;
  border-bottom: 1px solid #e8e8e8;

  .chat-list-left-bot {
    font-size: 28rpx;
    margin: 18rpx 0rpx;
    color: #707070;
    line-height: 40rpx;
  }
}

.chat-list-box {
  display: flex;
  justify-content: space-between;
  // align-items: center;

  .chat-list-left-top {
    font-size: 28rpx;
    font-weight: 500;
    color: #000000;
    line-height: 40rpx;
  }

  .chat-list-left-box {
    max-width: 85%;
  }

  .chat-list-right-box {
    padding-top: 10rpx;
  }

  .chat-list-action-box {
    display: flex;

    .btn-box {
      margin-left: 32rpx;

      &:first-child {
        margin-left: 0;
      }
    }
  }

  .chat-list-action {
    width: 28rpx;
    height: 28rpx;
    position: relative;
    top: 2rpx;
  }

  .chat-list-action_playing {
    // width: 22rpx;
    height: 32rpx;
    display: flex;
    align-items: center;
  }

  /* 新增样式 */
  .selectable-text {
    white-space: pre-wrap;
    // -webkit-user-select: text !important; // 添加 !important
    user-select: text !important; // 添加 !important
  }
}
</style>
