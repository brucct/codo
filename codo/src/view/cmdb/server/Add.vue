<template>
<!-- <div> -->
  <!-- <Card> -->
<Modal width="600px;" v-model="dialog.show"  :title="dialog.title" :loading=true :footer-hide=true @on-cancel="handleCancel">
    <Form ref="formData" :model="formData" :rules="ruleValidate" :label-width="80">
        <FormItem label="主机名" prop="hostname">
            <Input v-model="formData.hostname" placeholder=""></Input>
        </FormItem>

        <FormItem label="主机组" >
            <Transfer
            :data="GroupList"
            :target-keys="formData.group"
            filterable
            :filter-method="groupFilter"
            :titles="groupTitle"
            @on-change="groupHandleChange">
            </Transfer>
        </FormItem>

        <FormItem label="IDC">
            <Select v-model="formData.idc" placeholder="请选择" filterable>
                <Option value="qcloud" >腾讯云</Option>
                <Option value="aliyun" >阿里云</Option>
                <Option value="aws" >AWS</Option>
                <Option value="internal" >内网</Option>
                <Option value="other" >其他</Option>
            </Select>
        </FormItem>

        <FormItem label="区域">
            <Input v-model="formData.region" placeholder=""></Input>
        </FormItem>

        <FormItem label="管理用户">
            <Row>
                <Col span="4">
                    <Checkbox v-model="single">手动录入</Checkbox>

                </Col>
                <Col span="8" offset="1" v-show="!single">
                    <Select v-model="formData.admin_user" placeholder="请选择" filterable>
                        <Option v-for="item in AdmUser" :value="item.id">{{item.name}}</Option>
                    </Select>
                </Col>

            </Row>
            <Row v-show="single">
                <Col span="11"><Input v-model="formData.username" placeholder="用户名"></Input></Col>
                <Col span="11" offset="2"><Input v-model="formData.password" placeholder="密码"></Input></Col>
            </Row>

        </FormItem>

        <FormItem label="Public_IP" prop="public_ip">
            <Input v-model="formData.public_ip" placeholder=""></Input>
        </FormItem>

        <FormItem label="Private_IP" prop="private_ip">
            <Input v-model="formData.private_ip" placeholder=""></Input>
        </FormItem>

        <FormItem label="Port">
            <Input v-model="formData.port" placeholder=""></Input>
        </FormItem>

        <FormItem label="CPU">
            <Input v-model="formData.cpu" placeholder=""></Input>
        </FormItem>

        <FormItem label="Memory">
            <Input v-model="formData.memory" placeholder=""></Input>
        </FormItem>

        <FormItem label="Disk">
            <Input v-model="formData.disk" placeholder=""></Input>
        </FormItem>

        <FormItem label="系统类型">
            <Select v-model="formData.os_platform" placeholder="请选择" filterable>
                <Option value="Linux" >Linux</Option>
                <Option value="Windows" >Windows</Option>
                <Option value="Other" >Other</Option>
            </Select>
        </FormItem>

        <FormItem label="系统版本">
            <Input v-model="formData.os_version" placeholder=""></Input>
        </FormItem>

        <FormItem label="SN">
            <Input v-model="formData.sn" placeholder=""></Input>
        </FormItem>

        <FormItem label="主机描述">
            <Input v-model="formData.comment" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder=""></Input>
        </FormItem>

        <FormItem label="Tag标签" >
            <Transfer
            :data="TagList"
            :target-keys="formData.tag"
            filterable
            :filter-method="tagFilter"
            :titles="tagTitle"
            @on-change="tagHandleChange">
            </Transfer>
        </FormItem>

        <FormItem>
            <Button type="primary" @click="handleSubmit('formData')">提交</Button>
            <Button @click="handleReset('formData')" style="margin-left: 8px">重置</Button>
        </FormItem>
    </Form>
</Modal>
  <!-- </Card>     -->
<!-- </div> -->
</template>
<script>
import { getAdmUser, getGroupList, getTagList, addProject } from '@/api/cmdb/server'
// import { getAppList } from '@/api/app'
export default {
  name: 'add',
  data () {
    return {
      single: false,
      GroupList: [],
      TagList: [],
      groupTitle: ['可关联', '已关联'],
      tagTitle: ['可关联', '已关联'],
      AdmUser: [],
      ruleValidate: {
        hostname: [
          { required: true, message: '项目名称不能为空', trigger: 'blur' }
        ],
        public_ip: [
          { required: true, message: 'IP不能为空', trigger: 'blur' }
        ],
        port: [
          { required: true, message: '端口不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    groupHandleChange (newTargetKeys) {
      console.log(this.formData.group)
      this.formData.group = newTargetKeys
    },
    groupFilter (data, query) {
      return data.label.indexOf(query) > -1
    },
    tagHandleChange (newTargetKeys) {
      console.log(this.formData.tag)
      this.formData.tag = newTargetKeys
    },
    tagFilter (data, query) {
      return data.label.indexOf(query) > -1
    },
    handleCancel () {
      this.$emit('e-close')
    },
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          // add => post => /api/cmdb/server/
          // edit => put => /api/cmdb/server/1
          console.log(this.formData)
          const url = this.dialog.option == 'add' ? '/' : `/${this.formData.id}/`
          const action = this.dialog.option == 'add' ? 'post' : 'put'
          const msg = this.dialog.option == 'add' ? '主机添加成功' : '主机修改成功'
          addProject(this.formData, url, action).then(res => {
            console.log(res)
            if (res.status) {
              this.$Message.success({
                content: msg,
                duration: 3
              })
              this.$emit('e-close')
              this.$emit('e-update')
            } else {
              this.$Message.error({
                content: res.data.msg,
                duration: 3
              })
            }
          }).catch(error => {
            this.$Message.error({
              content: JSON.stringify(error.response.data),
              duration: 10
            })
          })
        } else {
          this.$Message.error({
            content: '请检查必选项',
            duration: 3
          })
        }
      })
    },
    handleReset (name) {
      console.log('name..', name)
      this.$refs[name].resetFields()
    }

  },
  props: {
    dialog: Object,
    formData: Object
  },
  watch: {
    formData: function () {
      this.single = this.formData.single
    },
    single: function () {
      if (this.single == false) {
        this.formData.username = null
        this.formData.password = null
      }
    }
  },
  mounted () {
    getGroupList().then(res => {
      const data = res.data
      for (var item in data) {
        this.GroupList.push({
          key: data[item].id,
          label: data[item].name
        })
      }
    }),
    getTagList().then(res => {
      const data = res.data
      for (var item in data) {
        this.TagList.push({
          key: data[item].id,
          label: data[item].name
        })
      }
    }),
    getAdmUser().then(res => {
      this.AdmUser = res.data
      console.log(this.AdmUser)
    })
  }

}
</script>
