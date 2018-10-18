# 返回错误信息表单


class FormMixin(object):
    def get_error(self):
        if hasattr(self, 'errors'):
            errors = self.errors.get_json_data()
            print(errors)
            if errors != {}:
                # {"telephone":[{"message":"手机号码的个数必须位11位！"}]}
                error_tuple = errors.popitem()
                error_list = error_tuple[1]
                error_dict = error_list[0]
                message = error_dict['message']
                return message
            else:
                return None
        else:
            return None
