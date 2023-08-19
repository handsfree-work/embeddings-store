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

  const statusDict = dict({
    data: [
      { value: "1", label: "开启", color: "success" },
      { value: "2", label: "停止", color: "blue" },
      { value: "0", label: "关闭", color: "blue" }
    ]
  });

  const remoteDict = dict({
    url: "/mock/dicts/OpenStatusEnum",
    immediate: false
  });
  // remoteDict.loadDict();

  return {
    remoteDict,
    crudOptions: {
      request: {
        pageRequest,
        addRequest,
        editRequest,
        delRequest
      },
      columns: {
        id: {
          title: "ID",
          key: "id",
          type: "number",
          column: {
            width: 50
          },
          form: {
            show: false
          }
        },
        status: {
          title: "本地字典",
          search: { show: false },
          dict: statusDict,
          type: "dict-select"
        },
        remote: {
          title: "远程字典",
          search: { show: true },
          dict: remoteDict,
          type: "dict-select",
          column: {
            component: {
              onDictChange(opts: any) {
                console.log("字典变化：", opts);
              }
            }
          }
        },
        modifyDict: {
          title: "动态修改字典",
          search: { show: false },
          type: "text",
          form: {
            component: {
              name: "a-switch",
              vModel: "checked"
            },
            valueChange({ form }) {
              console.log("changed", form.modifyDict);
              remoteDict.url = form.modifyDict ? "/mock/dicts/moreOpenStatusEnum?remote" : "/mock/dicts/OpenStatusEnum?remote";
              // 由于remoteDict.cloneable =false,所以全局公用一个实例，修改会影响全部地方
              remoteDict.reloadDict();
            }
          },
          column: {
            component: {
              name: "a-switch",
              vModel: "checked",
              on: {
                // 注意：必须要on前缀
                onChange({ $event }) {
                  remoteDict.url = $event ? "/mock/dicts/moreOpenStatusEnum?remote" : "/mock/dicts/OpenStatusEnum?remote";
                  remoteDict.reloadDict();
                }
              }
            }
          }
        }
      }
    }
  };
}
