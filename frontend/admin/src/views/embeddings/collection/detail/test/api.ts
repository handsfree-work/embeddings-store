//@ts-ignore
import { request } from "/src/api/service";
const apiPrefix = "/admin/embeddings/document";
export async function DoSearch(form: {
  query:string,
  collection_id:number,
  limit:number,
}) {
  return request({
    url: apiPrefix + "/search",
    method: "post",
    data: {
      ...form
    }
  });
}
