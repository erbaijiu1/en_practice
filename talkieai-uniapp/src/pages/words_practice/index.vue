
<template>
  <view>
    <CommonHeader title="Talkie">
      <template v-slot:content>
        <text>练习</text>
      </template>
    </CommonHeader>
    <view class="content">
      <view class="chat-tab-box">
        <view v-for="i in 6" :key="i" :class="`chat-tab ${tabNum === i ? 'chat-tab-actice' : ''}` " @tap="tabChange(i)">
          list {{ i }}
        </view>
      </view>
      <view class="chat-tab-content">
        <block v-for="([each_list_id, module_list]) in totalContens" :key="each_list_id">
          <scroll-view :id="`hat-tab-content-${each_list_id}`" scroll-y="true" @scrolltolower="onScroll"
            v-show="tabNum === each_list_id"
            class="chat-tab-content-item">

            <view v-for="([key, content_details]) in module_list" :key="key">

              <view class="module_title">
                {{ key }}
              </view>

              <Statement v-for="sentence in content_details" :collect="sentence" :cannotCancel="false" />

            </view>

          </scroll-view>

        </block>

      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { onShow } from "@dcloudio/uni-app";

import LoadingRound from "@/components/LoadingRound.vue";
import CommonHeader from "@/components/CommonHeader.vue";
import type { PracticeSentence } from "@/models/models";
import Single from "./components/Single.vue";
import Statement from "./components/Statement.vue";
import accountRequest from "@/api/account";
import wordsPracticeRequest from "@/api/words_practice";

const tabNum = ref<number>(1);
// const senPageSize = ref<number>(1);
// const sentenceLoading = ref<boolean>(false);
const oneListContents = ref<Map<string, PracticeSentence[]>>(new Map());
const totalContens = ref<Map<number, any>>(new Map());


onMounted(() => {
  uni.setNavigationBarTitle({
    title: 'TalkieAI'
  });
});

onShow(() => {
  nextTick(() => {
    initData();
  });
});

const handleDeleteCollect = (id: number) => {
  initData();
};

const initData = () => {
  // senPageSize.value = 1;

  get_practice_list(tabNum.value);
}

const get_practice_list = (list_id: number) => {
  let param = {"list_id": list_id}
  wordsPracticeRequest.getWordsList(param).then((data) => {
    console.log(list_id, ",data:", data);

    oneListContents.value.clear();
    data.data.items.forEach((item: any) => {
      try {
        const details = JSON.parse(item.details); // 解析 details

        const content_details = ref<PracticeSentence[]>([]);
        details.forEach((detail: {en: string, cn: string, struct: string, words: string}) => {
          content_details.value.push({
            content: detail.en,
            translation: detail.cn,
            message_id: null,
            type: "SENTENCE",
            struct:detail.struct,
            words:detail.words
          });
        })
       
        oneListContents.value.set(item.main_words, content_details.value);
        console.log("oneListContents:", oneListContents.value);

      } catch (parseError) {
        console.error("Failed to parse details for item:", item.id, parseError);
      }
    });

    if (totalContens.value.has(list_id)) {
          const oldOneListContents = totalContens.value.get(list_id);
          totalContens.value.set(list_id, new Map([...oldOneListContents, ...oneListContents.value]));
        } else {
          totalContens.value.set(Number(list_id), oneListContents.value);
        }

  });
}

const refreshData = () => {
  // senPageSize.value = 1;
}


const tabChange = (type: number) => {
  tabNum.value = type;

  get_practice_list(type);
};

const onScroll = (event: any) => {
  get_practice_list(tabNum.value);
};
</script>

<style lang="scss">
.content {
  display: flex;
  flex-direction: column;
}

.goods-carts {
  /* #ifndef APP-NVUE */
  display: flex;
  /* #endif */
  flex-direction: column;
  position: fixed;
  left: 0;
  right: 0;
  /* #ifdef H5 */
  left: var(--window-left);
  right: var(--window-right);
  /* #endif */
  bottom: 0;
}

.logo {
  height: 200rpx;
  width: 200rpx;
  margin-top: 200rpx;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 50rpx;
}

.text-area {
  display: flex;
  justify-content: center;
}

.title {
  font-size: 36rpx;
  color: #8f8f94;
}

.module_title{
  font-size: 24rpx;
  background-color: #e3e3e3;
  padding: 6rpx 16rpx;
}

.chat-tab-content {
  overflow-x: hidden;
}

.chat-tab-box {
  display: flex;
  padding: 32rpx;
  align-items: center;
  overflow-x: auto;

  .chat-tab {
    margin-right: 44rpx;
    font-size: 36rpx;
    position: relative;
    display: flex;
    justify-content: center;
    transition: 0.1s all linear;
    height: 50rpx;
    line-height: 50rpx;
  }

  .chat-tab-actice {
    font-size: 42rpx;
    font-weight: 500;
  }

  .chat-tab-actice::after {
    position: absolute;
    content: "";
    background: #6236ff;
    width: 40rpx;
    height: 10rpx;
    border-radius: 5rpx;
    bottom: -20rpx;
  }
}
</style>
