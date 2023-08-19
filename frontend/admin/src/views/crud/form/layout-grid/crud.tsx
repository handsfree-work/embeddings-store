import * as api from "./api";
import { AddReq, CreateCrudOptionsProps, CreateCrudOptionsRet, DelReq, EditReq, UserPageQuery, UserPageRes } from "@fast-crud/fast-crud";
export default function ({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
  const pageRequest = async (query: UserPageQuery): Promise<UserPageRes> => {
    return await api.GetList(query);
  };
  const editRequest = async ({ form, row }: EditReq) => {
    form.id = row.id;
    return await api.UpdateObj(form);
  };
  const delRequest = async ({ row }: DelReq) => {
    return await api.DelObj(row.id);
  };

  const addRequest = async ({ form }: AddReq) => {
    return await api.AddObj(form);
  };

  return {
    crudOptions: {
      request: {
        pageRequest,
        addRequest,
        editRequest,
        delRequest
      },
      form: {
        // 具体可配置请参考 grid 布局： http://www.ruanyifeng.com/blog/2019/03/grid-layout-tutorial.html
        display: "grid"
      },
      columns: {
        avatar: {
          title: "头像上传",
          type: "avatar-uploader",
          form: {
            order: 0,
            col: {
              style: { gridRow: "span 3" }
            },
            helper: "通过grid布局，可以实现比flex更加规整的排列"
          }
        },
        name: {
          title: "姓名",
          type: "text",
          search: { show: true }
        },
        order: {
          title: "占位演示",
          type: "text"
        },
        place: {
          title: "占位演示",
          type: "text"
        },
        intro: {
          title: "跨列",
          type: "textarea",
          form: {
            col: {
              style: { gridColumn: "span 2" } // grid 模式控制跨列
            }
          }
        }
      }
    }
  };
}
