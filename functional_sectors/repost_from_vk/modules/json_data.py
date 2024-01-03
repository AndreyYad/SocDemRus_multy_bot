from json import load, dump

json_path = 'functional_sectors/repost_from_vk/json/data.json'

async def _get_json():
    with open(json_path) as file:
        return load(fp=file)
    
async def get_saved_id_last_post():
    return (await _get_json())['last_post_id']

async def save_post_id(post_id: int):
    json_data = await _get_json()
    json_data['last_post_id'] = post_id
    with open(json_path, 'w') as file:
        dump(obj=json_data, fp=file, indent=4)

async def get_already_sent():
    return (await _get_json())['already_sent']

async def set_send_status(new_status: bool):
    json_data = await _get_json()
    json_data['already_sent'] = new_status
    with open(json_path, 'w') as file:
        dump(obj=json_data, fp=file, indent=4)