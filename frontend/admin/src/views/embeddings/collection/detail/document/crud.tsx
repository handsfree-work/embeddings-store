import * as api from "./api";
import { AddReq, CreateCrudOptionsProps, CreateCrudOptionsRet, DelReq, dict, EditReq, UserPageQuery, UserPageRes } from "@fast-crud/fast-crud";

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
      rowHandle: {
        fixed: "right"
      },
      table: {
        scroll: {
          //使用固定列时需要设置此值，并且大于等于列宽度之和的值
          x: 1400
        }
      },
      toolbar:{
        compact:false
      },
      columns: {
        id: {
          title: "id",
          type: "text",
          form: { show: false }, // 表单配置
          column: {
            width: 70,
            sorter: true
          }
        },
        key: {
          title: "集合Key",
          type: "text",
          search: { show: true }, // 开启查询
          form: {
            rules: [
              { required: true, message: "请输入集合Key" },
              { max: 50, message: "最大50个字符" }
            ]
          },
          editForm: { component: { disabled: true } },
          column: {
            sorter: true
          }
        },
        title: {
          title: "集合名称",
          type: "text",
          search: { show: true }, // 开启查询
          form: {
            rules: [
              { required: true, message: "请输入集合名称" },
              { max: 50, message: "最大50个字符" }
            ]
          },
          editForm: { component: { disabled: true } },
          column: {
            sorter: true
          }
        },
        remark: {
          title: "备注",
          type: "text",
          column: {
            sorter: true
          },
          form: {
            rules: [{ max: 100, message: "最大100个字符" }]
          }
        },
        created_at: {
          title: "创建时间",
          type: "datetime",
          form: { show: false }, // 表单配置
          column: {
            width: 180,
            sorter: true
          }
        },
        updated_at: {
          title: "修改时间",
          type: "datetime",
          form: { show: false }, // 表单配置
          column: {
            sortable: "update_time",
            width: 180
          }
        },
      }
    }
  };
}
