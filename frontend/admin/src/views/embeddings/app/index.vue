<template>
  <fs-page class="page-em-app">
    <template #header>
      <span class="title">
        APP管理
        <span class="sub">接口token创建与管理</span>
      </span>

    </template>
    <fs-crud ref="crudRef" v-bind="crudBinding" />
  </fs-page>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useCrud, useExpose, useFs } from "@fast-crud/fast-crud";
import createCrudOptions from "./crud";
export default defineComponent({
  name: "EmbeddingsApp",
  props:{
    id:{
      type: Number,
      required:true
    }
  },
  setup() {
    // 初始化crud配置
    // 此处传入权限前缀进行通用按钮权限设置，会通过commonOptions去设置actionbar和rowHandle的按钮的show属性
    // 更多关于按钮权限的源代码设置，请参考 ./src/plugin/fast-crud/index.js （75-77行）
    const { crudBinding, crudRef, crudExpose } = useFs({ createCrudOptions, context: { permission: "authority:user" } });

    // 页面打开后获取列表数据
    onMounted(() => {
      crudExpose.doRefresh();
    });

    return {
      crudBinding,
      crudRef
    };
  }
});
</script>
