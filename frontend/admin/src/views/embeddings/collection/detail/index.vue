<template>
  <fs-page class="page-em-collection-detail">
    <template #header>
      <div class="title">知识库
        <span class="sub">{{info.title}}【{{info.key}}】</span>
      </div>
    </template>

    <div class="body">
      <a-tabs v-model:activeKey="activeKey" tabPosition="left">
        <a-tab-pane v-for="item of tabs " :key="item.key" :tab="item.title">
          <fs-render :renderFunc="item.render"></fs-render>
        </a-tab-pane>
      </a-tabs>
    </div>
  </fs-page>
</template>

<script lang="tsx" setup>

import {nextTick, onMounted, Ref, ref} from "vue";
import FsEmCollectionDocument from "./document/index.vue";
import FsEmCollectionSource from "./source/index.vue";
import FsEmCollectionTest from "./test/index.vue";
import FsEmCollectionImport from "./import/index.vue";
import {useRoute} from "vue-router";
import {usePageStore} from "/@/store/modules/page";
import {GetObj} from "/@/views/embeddings/collection/detail/api";

const activeKey = ref("document")
const route = useRoute()
const id = parseInt(route.query.id as string)
const tabs = ref([
  // {
  //   key: 'import',
  //   title: '导入数据',
  //   render(){
  //     return <FsEmCollectionImport id={id}/>
  //   }
  // },
  {
    key: 'document',
    title: '知识库数据',
    render(){
      return <FsEmCollectionDocument id={id}/>
    }
  },
  // {
  //   key: 'source',
  //   title: '数据源',
  //   render(){
  //     return <FsEmCollectionSource id={id}/>
  //   }
  // },
  {
    key: 'test',
    title: '查询测试',
    render(){
      return <FsEmCollectionTest id={id}/>
    }
  },
  // {
  //   key: 'setting',
  //   title: '设置',
  //   render(){
  //     return <FsEmCollectionSource id={id}/>
  //   }
  // }
  ])

const info:Ref = ref({})

const loadInfo = async ()=>{
  info.value = await GetObj(id)
}

const pageStore = usePageStore();
onMounted(async ()=>{
  await nextTick()
  await loadInfo()
  const title = info.value?.title
  if (title){
    pageStore.updateTitle({"title":"知识库详情:"+title,fullPath:route.fullPath})
  }
})


</script>
<style lang="less">
.page-em-collection-detail{
  .body{
    display: flex;
    height: 100%;
    width: 100%;
    .ant-tabs{
      width:100%;
      height: 100%;
      .ant-tabs-nav{
        padding-top:20px;
      }
      .ant-tabs-content-holder{
        height: 100%;
        .ant-tabs-content{
          height: 100%;
          .ant-tabs-tabpane{
            height: 100%;
            position: relative;
            padding-left: 0px;
          }
        }
      }

    }
  }
}
</style>
