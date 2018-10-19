# 返回错误信息表单
class FormMixin(object):
    def get_error(self):
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            print(errors)
            # 打印结果： {"telephone":[{"message":"手机号码的个数必须位11位！"}]}
            if errors != {}:
                error_tuple = errors.popitem()
                error_list = error_tuple[1]
                error_dict = error_list[0]
                message = error_dict['message']
                print(message)
                # 打印结果：手机号码的个数必须位11位！
                return message
            else:
                return None
        else:
            return None
