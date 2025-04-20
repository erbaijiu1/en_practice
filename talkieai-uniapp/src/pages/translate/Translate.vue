<template>
  <view class="container">
    <input 
      class="input-box"
      v-model="inputText"
      placeholder="Enter English/Chinese text..."
      type="text"
      @input="handleInput"
    />
    <button @click="translate" class="translate-btn">Translate</button>

    <view v-if="showResult" class="result-section">
      <view class="result-item">
        <text class="label">English:</text>
        <text class="content">{{ result.english }}</text>
      </view>
      <view class="result-item">
        <text class="label">Pronunciation:</text>
        <text class="content">{{ result.pronunciation }}</text>
      </view>
      <view class="result-item">
        <text class="label">Chinese:</text>
        <text class="content">{{ result.chinese }}</text>
      </view>
      <view class="examples">
        <text class="examples-label">Examples:</text>
        <block v-for="(example, index) in examples" :key="index">
          <view class="example-item">
            {{ example }}
          </view>
        </block>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      inputText: '',
      showResult: false,
      result: {
        english: '',
        pronunciation: '',
        chinese: ''
      },
      examples: []
    };
  },
  methods: {
    handleInput() {
      // Input validation can be added here
    },
    translate() {
      // Temporary mock data - should be replaced with real API calls
      this.showResult = true;
      this.result = {
        english: this.inputText.includes(' ') ? this.inputText : 'hello',
        pronunciation: '/həˈloʊ/',
        chinese: this.inputText.includes(' ') ? this.inputText : '你好'
      };
      this.examples = [
        'Hello, how are you?',
        'Hello world!',
        'Good morning, hello!'
      ];
    }
  }
};
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
</style>