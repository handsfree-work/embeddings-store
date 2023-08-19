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
        title: "用户管理",
        name: "user",
        meta: {
          icon: "ion:person-outline",
          permission: "authority:user:view"
        },
        path: "/sys/authority/user",
        component: "/sys/authority/user/index.vue"
      }
    ]
  }
];
