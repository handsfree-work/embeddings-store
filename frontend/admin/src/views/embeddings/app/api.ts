//@ts-ignore
import { request } from "/src/api/service";
const apiPrefix = "/admin/embeddings/app";
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
