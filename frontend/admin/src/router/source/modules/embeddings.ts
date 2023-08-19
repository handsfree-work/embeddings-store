//@ts-ignore
import LayoutPass from "/src/layout/layout-pass.vue";

export const embeddingsResources = [
  {
    title: "嵌入管理",
    name: "embeddings",
    path: "/embeddings",
    redirect: "/embeddings/tes",
    component: LayoutPass,
    meta: {
      icon: "ion:settings-outline",
      permission: "admin"
    },
    children: [
      {
        title: "集合管理",
        name: "embeddings-collection",
        meta: {
          icon: "ion:person-outline",
          permission: "embeddings:collection:view"
        },
        path: "/embeddings/collection",
        component: "/embeddings/collection/index.vue"
      }
    ]
  }
];
