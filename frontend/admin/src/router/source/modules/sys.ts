import LayoutPass from "/@/layout/layout-pass.vue";

export const sysResources = [
  {
    title: "系统管理",
    name: "sys",
    path: "/sys",
    redirect: "/sys/authority/user",
    component: LayoutPass,
    meta: {
      icon: "ion:settings-outline",
      permission: "admin"
    },
    children: [
      {
        title: "权限资源管理",
        name: "permission",
        meta: {
          icon: "ion:list-outline",
          //需要校验权限
          permission: "authority:permission:view"
        },
        path: "/sys/authority/permission",
        component: "/sys/authority/permission/index.vue"
      },
      {
        title: "角色管理",
        name: "role",
        meta: {
          icon: "ion:people-outline",
          permission: "authority:role:view"
        },
        path: "/sys/authority/role",
        component: "/sys/authority/role/index.vue"
      },
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
