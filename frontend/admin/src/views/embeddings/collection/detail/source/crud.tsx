import * as api from "./api";
import { AddReq, CreateCrudOptionsProps, CreateCrudOptionsRet, DelReq, dict, EditReq, UserPageQuery, UserPageRes } from "@fast-crud/fast-crud";

export default function ({ crudExpose,context }: CreateCrudOptionsProps): CreateCrudOptionsRet {
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
  const {props} = context
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
      search:{
        initialForm:{
          collection_id:props.id,
        }
      },
      form:{
        group:{
          type:'collapse',
          accordion:false,
          groups:{
            base:{
              header:'数据源',
              columns:['source_type','resolve_config.file','title']
            },
            config:{
              header:'解析配置',
              columns:['resolve_config','resolve_type','content']
            }
          }

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
          title: "数据源标题",
          type: "text",
          search: { show: true }, // 开启查询
          form: {
            rules: [
              { required: true, message: "请输入数据源名称" },
              { max: 500, message: "最大500个字符" }
            ]
          },
          editForm: { component: { disabled: true } },
          column: {
            sorter: true
          }
        },
        source_type: {
          title: "数据源类型",
          type: "dict-select",
          search: { show: true }, // 开启查询
          dict:dict({
            data:[
              {value:'file',label:'文档上传'},
              {value:'csv',label:'csv'},
              {value:'text',label:'文本'},
              {value:'input',label:'手动分段输入'},
            ]
          }),
          form: {

          },
          column: {
            sorter: true
          }
        },
        resolve_type: {
          title: "解析方式",
          type: "dict-select",
          search: { show: true }, // 开启查询
          dict:dict({
            data:[
              {value:'GPT',label:'GPT智能解析分段'},
              {value:'direct_segment',label:'直接分段'},
              {value:'input',label:'手动分段输入'},
              {value:'direct_import',label:'直接导入'},
            ]
          }),
          form: {

          },
          column: {
            sorter: true
          }
        },
        resolve_config: {
          title: "解析配置",
          type: "text",
          column: {
            show:false,
            sorter: true
          },
          form:{
            value:{}
          }
        },
        'resolve_config.file':{
          title:"文件上传",
          type:'file-uploader',
          form:{
            component:{
              limit:1
            }
          },
          column:{
            show:false
          }
        },
        content:{
          title: "数据源内容",
          type: "text",
          column: {
            sorter: true
          }
        },
      }
    }
  };
}
