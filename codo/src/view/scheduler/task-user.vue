<template>
<Card style="height:100%">
  <Alert banner closable type="success">
    <h3>说明文档：</h3>
    <br/>
    <p>任务一般是通过ssh连接到远程主机执行，编排模板的时候会从此处选择执行用户，执行的时候会匹配系统用户的信息进行登录</p>
    <p>用户为ssh的时候使用的用户，端口为ssh端口，密钥为ssh的私钥，
      你需要把当对应公钥放入远端需要执行的主机，一般我们把CMDB里面的系统级管理用户导入，当作执行用户来使用</p>
  </Alert>
      <div class="search-con search-con-top">
      <Button type="primary"  @click="editModal('', 'post', '新建用户')" class="search-btn" >新建</Button>
    </div>
  <Table size="small" height="620" ref="selection" border :columns="columns" :data="tableData"></Table>
  <Modal v-model="modalMap.modalVisible"  :title="modalMap.modalTitle" :loading=true :footer-hide=true>
    <form-group :list="formList"  @on-submit-success="handleSubmit"></form-group>
  </Modal>
</Card>
</template>

<script>
import FormGroup from '_c/form-group'
import { getExecUserlist, operationExecUserlist } from '@/api/task'
export default {
  components: {
    FormGroup
  },
  data () {
    return {
      columns: [
        {
          title: '执行用户',
          key: 'alias_user',
          align: 'center',
          width: 150
        },
        {
          title: '系统用户',
          key: 'exec_user',
          align: 'center',
          width: 150
        },
        {
          title: 'SSH端口',
          key: 'ssh_port',
          align: 'center',
          width: 120
        },
        {
          title: '备注',
          key: 'remarks',
          align: 'center'
        },
        {
          title: '更新时间',
          key: 'update_time',
          width: 150
        },
        {
          title: '操作',
          key: 'handle',
          width: 150,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h(
                'Button',
                {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      this.editModal(params.index, 'put', '编辑用户')
                    }
                  }
                },
                '编辑'
              ),
              h(
                'Button',
                {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.delExecUser(params)
                    }
                  }
                },
                '删除'
              )
            ])
          }
        }
      ],
      tableData: [],
      modalMap: {
        modalVisible: false,
        modalTitle: '新建'
      },
      formList: [],
      editModalData: ''
    }
  },
  methods: {
    getExecUserList () {
      getExecUserlist().then(res => {
        if (res.data.code === 0) {
          this.tableData = res.data.data
        } else {
          this.$Message.error(`${res.data.msg}`)
        }
      })
    },
    editModal (index, meth, mtitle) {
      this.modalMap.modalVisible = true
      this.modalMap.modalTitle = mtitle
      this.editModalData = meth
      this.formList = [
        {
          name: 'id',
          value: meth === 'put' ? this.tableData[index].id : ''
        },
        {
          name: 'alias_user',
          type: 'i-input',
          maxlength: 80,
          value: meth === 'put' ? this.tableData[index].alias_user : '',
          label: '执行用户',

          placeholder: '请输入执行用户名称，编辑模板的时候会选择，必须使用英文字母',
          rule: [{ required: true, message: '执行用户名称不能为空', trigger: 'blur' }]
        },
        {
          name: 'exec_user',
          type: 'i-input',
          value: meth === 'put' ? this.tableData[index].exec_user : '',
          label: '系统用户',
          maxlength: 35,
          placeholder: '执行任务的时候会使用此用户来执行，必须使用英文字母',
          rule: [{ required: true, message: '系统用户名称不能为空', trigger: 'blur' }]
        },
        {
          name: 'ssh_port',
          type: 'i-input',
          value: meth === 'put' ? this.tableData[index].ssh_port : '22',
          label: 'SSH端口',
          maxlength: 5,
          placeholder: '请输入端口号，一般为22',
          rule: [
            { required: true, message: 'SSH端口不能为空', trigger: 'blur' }
          ]
        },
        {
          name: 'remarks',
          type: 'i-input',
          value: meth === 'put' ? this.tableData[index].remarks : '',
          label: '备注信息',
          maxlength: 120,
          placeholder: '请简单的备注一下。'
        },
        {
          name: 'user_key',
          type: 'i-input',
          type1: 'textarea',
          maxlength: 2500,
          value: meth === 'put' ? this.tableData[index].user_key : '',
          label: '用户私钥',
          placeholder: '请输入用户私钥，必填参数不能为空',
          rule: [
            { required: true, message: '用户私钥不能为空', trigger: 'blur' }
          ]
        }
      ]
    },
    handleSubmit (value) {
      setTimeout(() => {
        operationExecUserlist(value.data, this.editModalData).then(res => {
          if (res.data.code === 0) {
            this.$Message.success(`${res.data.msg}`)
            this.getExecUserList()
            this.modalMap.modalVisible = false
          } else {
            this.$Message.error(`${res.data.msg}`)
          }
        })
      }, 1000)
    },
    // 删除
    delExecUser (params) {
      if (confirm(`确定要删除 ${params.row.exec_user}`)) {
        operationExecUserlist({ exec_user_id: params.row.id }, 'delete').then(
          res => {
            if (res.data.code === 0) {
              this.$Message.success(`${res.data.msg}`)
              this.tableData.splice(params.index, 1)
            } else {
              this.$Message.error(`${res.data.msg}`)
            }
          }
        )
      }
    }
  },
  mounted () {
    this.getExecUserList()
  }
}
</script>

<style lang="less" scoped>
.search-con {
  padding: 10px 0;
  .search {
    &-col {
      display: inline-block;
      width: 200px;
    }
    &-input {
      display: inline-block;
      width: 200px;
      margin-left: 2px;
    }
    &-btn {
      margin-left: 2px;
    }
  }
}
</style>
