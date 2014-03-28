$$ send_file.send jade_module_view
$$ send_file.send jade_module_form
% for item in env['send_list']:
$$ send_file.send jade_module_prompt_${item}
% endfor