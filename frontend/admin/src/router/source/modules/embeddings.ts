//@ts-ignore
import LayoutPass from "/src/layout/layout-pass.vue";

export const embeddingsResources = [
  {
    title: "嵌入管理",
    name: "embeddings",
    path: "/embeddings",
    redirect: "/embeddings/collection",
    component: LayoutPass,
    meta: {
      icon: "ion:server-outline",
      permission: "admin"
    },
    children: [
      {
        title: "知识库管理",
        name: "embeddings-collection",
        meta: {
          icon: "ion:book-outline",
          permission: "embeddings:collection:view"
        },
        path: "/embeddings/collection",
        component: "/embeddings/collection/index.vue"
      },
      {
        title: "知识库详情",
        name: "embeddings-collection-index",
        meta: {
          icon: "ion:book-outline",
          permission: "embeddings:collection:view",
          isMenu: false
        },
        path: "collection/detail",
        component: "/embeddings/collection/detail/index.vue"
      },
      {
        title: "APP管理",
        name: "embeddings-app",
        meta: {
          icon: "ion:logo-apple-ar",
          permission: "embeddings:app:view"
        },
        path: "/embeddings/app",
        component: "/embeddings/app/index.vue"
      }
    ]
  }
];
