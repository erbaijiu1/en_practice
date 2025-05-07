<template>
  <view class="container">
    <input class="input-box" v-model="inputText" placeholder="Enter English/Chinese text..." type="text"
      @input="handleInput" />
    <button @click="translate" class="translate-btn">Translate</button>

    <view v-if="showResult" class="result-section">
      <view class="result-item">
        <!-- <text class="label">English:</text> -->
        <text class="content content_en">{{ result.english }}</text>
      </view>
      <view class="result-item">
        <!-- <text class="label">Pronunciation:</text> -->
        <text class="content">英 {{ result.pronunciation }}</text>
        <text v-if="result.pronunciation !== result.pronunciation_usa" class="content pronun_add">
          美 {{ result.pronunciation_usa }}
        </text>
      </view>
      <view class="result-item">
        <!-- <text class="label">Chinese:</text> -->
        <text class="content">{{ result.chinese }}</text>
      </view>

      <view class="examples">
        <!-- <text class="examples-label">Examples:</text> -->
        <Statement v-for="sentence in result.examples" :collect="sentence" :cannotCancel="false" />

        <block v-for="(example, index) in result.examples" :key="index">
          <view class="example-item">
            <text class="example-en">{{ example.en }}</text>
            <text class="example-cn">{{ example.cn }}</text>
          </view>
        </block>
      </view>
    </view>
  </view>
</template>

<script>

import chatRequest from '@/api/chat';
import { ref } from 'vue';
import Statement from "./components/Statement.vue";

export default {

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
      examples: []
    };
  },
  methods: {
    handleInput() {
      // Input validation can be added here
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
      chatRequest.wordDetail( {"word": this.inputText} ).then((res) => {
          // wordPhoneticSymbol.value = res.data.phonetic;
          // wordExplain.value = res.data.translation;
          this.wordDetailLoading = false;
          
          console.log(res.data);
          // Temporary mock data - should be replaced with real API calls
          this.result = {
            english: res.data.words_en,
            pronunciation: res.data.phonetic,
            chinese: res.data.translation,
            pronunciation_usa: res.data.phonetic_usa,
            examples: res.data.example
          };
          this.showResult = true;

          this.examples = [
            'Hello, how are you?',
            'Hello world!',
            'Good morning, hello!'
          ];

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

}

.examples{
  margin-top: 30rpx;
}

</style>