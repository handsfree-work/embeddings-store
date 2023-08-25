<template>
  <fs-page class="page-em-collection-detail-import">
    <template #header>
      <div class="title">数据导入</div>
    </template>

    <div class="body">
      <a-tabs v-model:activeKey="activeKey" >
        <a-tab-pane v-for="item of tabs " :key="item.key" :tab="item.title">
          <fs-render :renderFunc="item.render"></fs-render>
        </a-tab-pane>
      </a-tabs>
    </div>
  </fs-page>
</template>

<script lang="tsx" setup>

import {nextTick, onMounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {Modal, notification} from "ant-design-vue";
import {importTable, loadFsImportUtil} from "@fast-crud/fast-crud";

defineOptions({
  name:"FsEmCollectionDetailImport",
})

const props = defineProps({
  id:{
    type: Number,
    required:true
  }
})

const activeKey = ref("direct")


async function onCsvFileSelected(e: any) {
  const file = e.target.files[0];
  // do import
  const filename = file.name
  const importUtil = await loadFsImportUtil();
  const importData = await importUtil.csv(file);

  notification.success({
    message: "导入成功"
  });
}

const tabs = ref([
  {
    key: 'direct',
    title: '手动输入',
    render(){
      return <div>手动输入 {props.id}</div>
    }
  },
  {
    key: 'csv',
    title: 'csv导入',
    render(){
      return <div>
        <div>
          <p>
            1、点击下载<a href={"template-import.csv"}>导入模板</a>
          </p>
          <p>
            2、<span>模板填充数据</span>
          </p>
          <p>
            <span>3、导入：</span>
            <input type={"file"} onInput={onCsvFileSelected}></input>
          </p>
        </div>
      </div>
    }
  },
  {
    key: 'segment',
    title: '直接分段',
    render(){
      return <div>直接分段</div>
    }
  },
  {
    key: 'gpt',
    title: 'QA智能拆分',
    render(){
      return <div>QA智能拆分</div>
    }
  }])



</script>
<style lang="less">
.page-em-collection-detail-import {
  .body {
    display: flex;
    height: 100%;
    width: 100%;
    padding: 0 10px;
  }
}
</style>
