database_name = 'postgresql://user_vkinder:pass_vkinder@localhost:5432/vkinder'
with open('application/vk_token.txt', 'r', encoding='utf-8') as vk_file:
    token_group = vk_file.readline().strip()
    token_app = vk_file.readline().strip()
    id_group = vk_file.readline().strip()
