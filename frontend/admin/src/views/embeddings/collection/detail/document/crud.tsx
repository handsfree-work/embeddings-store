import * as api from "./api";
import { AddReq, CreateCrudOptionsProps, CreateCrudOptionsRet, DelReq, dict, EditReq, UserPageQuery, UserPageRes } from "@fast-crud/fast-crud";

export default function ({ crudExpose, context }: CreateCrudOptionsProps): CreateCrudOptionsRet {
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

  const { props } = context;
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
      toolbar: {
        compact: false
      },
      search: {
        initialForm: {
          collection_id: props.id
        }
      },
      form: {
        initialForm: {
          collection_id: props.id
        }
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
        title: {
          title: "标题",
          type: "textarea",
          search: { show: true }, // 开启查询
          form: {
            col: {
              span: 24
            },
            component: {
              placeholder: "问题",
              autoSize: { minRows: 3, maxRows: 6 }
            }
          },
          editForm: { component: { disabled: true } },
          column: {
            sorter: true
          }
        },
        content: {
          title: "内容",
          type: "textarea",
          search: { show: true }, // 开启查询
          form: {
            col: {
              span: 24
            },
            component: {
              placeholder: "答案",
              autoSize: { minRows: 4, maxRows: 8 }
            },
            helper: "以【title \\n content】格式拼接后计算向量数据"
          },
          editForm: { component: { disabled: true } },
          column: {
            sorter: true
          }
        },
        collection_id: {
          title: "集合",
          type: "dict-select",
          dict: dict({
            url: "/admin/embeddings/collection/list",
            label: "title",
            value: "id"
          }),
          form: {
            show: false
          },
          column: {
            sorter: true
          }
        }
        // source_id: {
        //   title: "数据源",
        //   type: "dict-select",
        //   column: {
        //     sorter: true
        //   },
        // },
        // source_index: {
        //   title: "源内序号",
        //   type: "number",
        //   column: {
        //     sorter: true
        //   },
        // },
      }
    }
  };
}
