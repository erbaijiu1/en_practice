<template>
  <view class="container">
    <input class="input-box" v-model="inputText" placeholder="Enter English/Chinese text..." type="text"
      @input="handleInput" />
    <button @click="translate" class="translate-btn">Translate</button>

    <!-- 加载中显示 Loading -->
    <LoadingRound v-if="wordDetailLoading" :min-height="200"></LoadingRound>

    <view v-else-if="showResult" class="result-section">
      <view class="result-item add_flex_too_side">
        <view class="add_flex">
          <!-- <text class="label">English:</text> -->
          <text class="content content_en">{{ result.english }}</text>
          <AudioPlayer class="pronunciation-play-icon icon_margin" :content="result.english" />
        </view>
        <view>
          <Collect type="WORD" :content="result.english" />

        </view>

      </view>

      <view class="result-item">
        <!-- <text class="label">Pronunciation:</text> -->
        <text class="content pronunciation_font ">英 {{ result.pronunciation }}</text>
        <text v-if="result.pronunciation !== result.pronunciation_usa" class="content pronun_add pronunciation_font">
          美 {{ result.pronunciation_usa }}
        </text>
      </view>
      <view class="result-item result_chiness">
        <!-- <text class="label">Chinese:</text> -->
        <text class="content">{{ result.chinese }}</text>
      </view>

      <view class="examples">
        <Statement v-for="(item, index) in translatedExamples" :key="index" :collect="item" :cannotCancel="false" />

        <!-- <block v-for="(item, index) in translatedExamples" :key="index">
          <view class="example-item">
            <text class="example-en">{{ item.en }}</text>
            <text class="example-cn">{{ item.cn }}</text>
          </view>
        </block> -->
      </view>
    </view>
  </view>
</template>

<script>

import chatRequest from '@/api/chat';
import { ref } from 'vue';
import Statement from "./components/Statement.vue";
import AudioPlayer from '@/components/AudioPlayer.vue';
import LoadingRound from '@/components/LoadingRound.vue';
import Collect from '@/components/Collect.vue';


export default {
  components: {
    Statement, // 👈 显式注册组件
    AudioPlayer
    ,  LoadingRound
    , Collect
  },

  data() {
    return {
      inputText: '',
      showResult: false,
      wordDetailLoading: false,
      result: {
        english: '',
        pronunciation: '',
        chinese: '',
        pronunciation_usa:'',
        examples: []
      },
      examples: [],
      wordDetailLoading: false,
      translatedExamples: []
    };
  },
  methods: {
    handleInput() {
      // Input validation can be added here
    },
    transformExamples(examples) {
      return examples.map(example => ({
        type: 'example',
        en: example.en,
        cn: example.cn
      }));
    },
    translate() {
      if (!this.inputText) {
        uni.showToast({
          title: 'Please enter text',
          icon: 'none'
        });
        return;
      }

      this.wordDetailLoading = true;
      chatRequest.wordDetail({ word: this.inputText }).then((res) => {
        console.log(res.data);

        // 设置 result 数据
        this.result = {
          english: res.data.words_en,
          pronunciation: res.data.phonetic,
          chinese: res.data.translation,
          pronunciation_usa: res.data.phonetic_usa,
          examples: res.data.example || []
        };

        this.wordDetailLoading = false;

        // 转换示例数据
        this.translatedExamples = this.transformExamples(this.result.examples);
        console.log("translatedExamples:", this.translatedExamples);

        this.showResult = true;
      });
    }
  }
}
</script>

<style>
.container {
  padding: 20rpx;
}
.input-box {
  height: 80rpx;
  border: 1rpx solid #ddd;
  padding: 20rpx;
  margin-bottom: 20rpx;
}
.translate-btn {
  background-color: #007AFF;
  color: white;
  margin: 30rpx 0;
}
.result-section {
  margin-top: 40rpx;
  padding: 20rpx;
  border: 1rpx solid #eee;
}
.result-item {
  margin-bottom: 20rpx;
}
.label {
  font-weight: bold;
  margin-right: 10rpx;
}
.examples-label {
  display: block;
  font-weight: bold;
  margin-bottom: 10rpx;
}
.example-item {
  margin-bottom: 15rpx;
  padding-left: 15rpx;
  border-left: 4rpx solid #007AFF;
}
.pronun_add{
  margin-left: 20rpx;
}

.example-en {
  display: block;
  font-weight: bold;
}

.example-cn {
  display: block;
  color: #666;
  margin-left: 20rpx;
}

.content_en{
  display: block;
  font-weight: bold;
  font-size: 1.5rem;
  font-weight: 700;

}

.examples{
  margin-top: 30rpx;
}


.add_flex{
  display: flex;
  align-items: center;
  
}
.icon_margin{
  margin-left: 30rpx;
}

.pronunciation_font{
  /* font-size: 1.2rem; */
  font-weight: 700;
  color: #999;
}

.add_flex_too_side{
  display: flex;
  justify-content: space-between;
  align-items: center;

}
.result_chiness{
  /* add under line */
  border-bottom: 1px solid #e8e8e8;
  padding: 20rpx 0;

}

</style>