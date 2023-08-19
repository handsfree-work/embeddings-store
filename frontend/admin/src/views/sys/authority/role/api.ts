import { request } from "/src/api/service";
const apiPrefix = "/admin/authority/role";
export async function GetList(query: any) {
  return request({
    url: apiPrefix + "/page",
    method: "post",
    data: query
  });
}

export async function AddObj(obj: any) {
  return request({
    url: apiPrefix + "/add",
    method: "post",
    data: obj
  });
}

export async function UpdateObj(obj: any) {
  return request({
    url: apiPrefix + "/update",
    method: "post",
    data: obj
  });
}

export async function DelObj(id: any) {
  return request({
    url: apiPrefix + "/delete",
    method: "post",
    params: { id }
  });
}

export async function GetObj(id: any) {
  return request({
    url: apiPrefix + "/info",
    method: "post",
    params: { id }
  });
}

/**
 * 获取角色权限资源
 * @param roleId
 * @returns {*}
 * @constructor
 */
export function getPermissionIds(roleId: any) {
  return request({
    url: apiPrefix + "/get_permission_ids",
    method: "post",
    params: { id: roleId }
  });
}

/**
 * 授权
 * @returns {*}
 * @constructor
 * @param role_id
 * @param permission_ids
 */
export function DoAuthz(role_id: any, permission_ids: any) {
  return request({
    url: apiPrefix + "/authz",
    method: "post",
    data: { role_id, permission_ids }
  });
}
