<template>
  <fs-page class="page-em-collection-detail-test">
    <div class="content">
      <div class="query">
        <a-input v-model:value="query" placeholder="输入关键字进行相似度匹配" @press-enter="search"></a-input>
        <a-input-number v-model:value="limit" title="限制数量"></a-input-number>
        <a-button type="primary" @click="search">测试</a-button>
      </div>

      <div class="results">
        <a-list item-layout="horizontal" :data-source="results" :loading="loading">
          <template #header> 查询结果： Total：{{ results.length }} </template>
          <template #renderItem="{ item }">
            <a-list-item>
              <a-list-item-meta>
                <template #title>
                  {{ item.title }}
                </template>
              </a-list-item-meta>
              <template #actions>
                <a-tag>id：{{ item.id }}</a-tag>
                <a-tag>score：{{ item.score }}</a-tag>
              </template>
              {{ item.content }}
            </a-list-item>
          </template>
        </a-list>
      </div>
    </div>
  </fs-page>
</template>

<script lang="ts" setup>
defineOptions({
  name: "FsEmCollectionTest"
});

import { ref } from "vue";
import { DoSearch } from "./api";

const props = defineProps<{
  id: number;
}>();

const query = ref("");
const limit = ref(10);
const loading = ref(false);
const results = ref([]);
const search = async () => {
  loading.value = true;
  try {
    const res = await DoSearch({
      query: query.value,
      collection_id: props.id,
      limit: limit.value
    });
    results.value = res.list;
  } finally {
    loading.value = false;
  }
};
</script>
<style lang="less">
.page-em-collection-detail-test {
  h4 {
    margin: 0;
  }
  .content {
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 20px;
    width: 50%;
    .query {
      display: flex;
      align-items: center;
      margin-bottom: 20px;
      > * {
        margin-right: 20px;
      }
    }
    .results {
      flex: 1;
      overflow-y: hidden;
      margin-top: 10px;
      .ant-list {
        height: 100%;
        display: flex;
        flex-direction: column;
        .ant-spin-nested-loading {
          flex: 1;
          height: 100%;
          overflow-y: auto;
        }
      }
    }
  }
}
</style>
