import * as api from "./api";
import { AddReq, CreateCrudOptionsProps, CreateCrudOptionsRet, DelReq, dict, EditReq, UserPageQuery, UserPageRes } from "@fast-crud/fast-crud";
import { useRouter } from "vue-router";
import { message } from "ant-design-vue";
import { SyncOutlined } from "@ant-design/icons-vue";

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

  const router = useRouter();
  const areaDict = dict({
    value: "id",
    label: "area",
    url: "/mock/FormInnerArea/all"
  });
  return {
    crudOptions: {
      request: {
        pageRequest,
        addRequest,
        editRequest,
        delRequest
      },
      form: {
        wrapper: {
          inner: true
        }
      },
      columns: {
        name: {
          title: "姓名",
          type: "text"
        },
        age: {
          title: "年龄",
          type: "text"
        },
        area: {
          title: "地区",
          type: "dict-select",
          dict: areaDict,
          form: {
            suffixRender() {
              function refresh() {
                message.info("刷新dict");
                areaDict.reloadDict();
              }
              function gotoAddArea() {
                message.info("调用 router.push 打开地区管理页面");
                router.push({ path: "/crud/form/inner/area" });
              }
              return (
                <a-button-group style={"padding-left:5px"}>
                  <a-button onClick={refresh}>
                    <SyncOutlined />
                  </a-button>
                  <a-button onClick={gotoAddArea}>添加地区</a-button>
                </a-button-group>
              );
            }
          }
        }
      }
    }
  };
}
