TEST_POPULATE_DB_WITH_PROMOTIONS_EXPECTED = [
    "4aeecc6e-efe2-4569-9269-cdd449042c38",
    "4c8c6640-37b4-42df-bb03-4e55332b44d4",
    "f4b955ed-1439-4b79-89de-f30db9e297de",
    "d8bf534f-f0fb-453a-83b0-242325bb82cd",
    "44efd174-00ea-4815-922f-f9d5ae4701ab",
    "c87d8d67-b0af-4513-88fe-88cea98ce0a8",
    "3d188c7f-3570-4ddd-a197-0ea6631462cf",
    "1e1ab167-9e8c-4210-ac8e-fbe0f2a0d277",
    "a5605a97-41ea-44c9-a28b-b87965cc099d",
    "cbc0b16e-3276-4808-9ec8-da8c3bdc2bd1",
    "ff643532-a257-405d-b939-7ce7999151fd",
    "1a680815-3941-4010-889f-700d62ab889e",
    "2a46c23c-b51e-4f53-96cd-e9c1843780ef",
    "24ba7215-016c-4b42-ba98-b47c0d8f1f6a",
    "a0ca6020-5709-45db-9af5-da4edce993eb",
    "23c6c690-3b02-45bc-962e-2209d4ddbe13",
    "6cb4de4c-ae81-4e6b-ba13-914a897c770f",
    "5e38cefb-7c15-4d23-ae02-5abb25a48438",
    "a0427ed2-3a48-4d5a-9574-ccd2f8a348a2",
    "e5772ec0-ba41-4239-9ec9-fb11b8d355d0",
    "3099daec-133e-448a-85f7-e942ffa96eef",
    "06b9eedf-32ad-4caf-a4d1-1a4a52b4e391",
    "ca3271d8-a3a3-47bc-bd2f-d0e87dcdcede",
    "8cb54fd3-9810-4816-b57d-c1a848411be1",
    "77ae5b7b-59b0-4560-a931-a10161e48bc1",
    "bc9bd6d1-5cd4-4178-bc52-e8572c1712b6",
    "cea0372e-9b4a-4039-91db-25fb772c1e36",
    "29ef85d7-208c-49c5-b577-c98d9eabe29d",
    "367d8573-9806-46bb-9a08-27a228e8289e",
    "95ece324-04ec-4064-ae80-58916a83ed2e",
    "1111d771-03c3-477f-9fd0-21ab53afc6d2",
    "c9169802-f1ad-44fe-bba9-5769b9cc50ba",
    "959aec88-8aa1-4d28-9ba7-eca19f10159e",
    "aa0b4cad-eb58-4514-b0d2-baf2a8cefcd5",
    "c919de8c-32eb-4b33-ae99-8375fa438447",
    "5434a0d0-d518-4a71-abe2-c5712ea58e7f",
    "abb7a630-8947-45c0-a100-76a0d1f3fabf",
    "c4716ead-35c7-4e21-a35f-02e002e90279",
    "fb13ad67-83c0-4baf-bec6-7452b55c1041",
    "d8dfd0ff-4ef3-469c-ad08-a4c094570eeb",
    "6055e7f1-fe58-43dd-8664-17b015b683f6",
    "c08d5912-98d8-4814-a402-18ad6abc0af7",
    "24fa85aa-6309-49d3-ab9d-86cbbd24bda7",
    "ed6efca1-37b6-491f-ba74-27168f9028a4",
    "8939446e-9f63-49eb-9030-4d97bd3ce943",
    "215dfe1d-ed62-4a07-b8bf-71176d8b47fc",
    "4a35568b-db06-4798-b7ca-07a35ae03c72",
    "c20367cd-67f8-40e5-8fe1-869264dc4e16",
    "bef2d021-06a8-44ff-a0b8-0ec73d571431",
    "b80e004e-dcb5-4110-bc63-f0f1f10eb7aa",
]

TEST_GET_PROMOTION_TAGS_REGEX_PARAMS = [
    (
        '[App] Monitor Gamer Curvo Samsung Odyssey 27" WQHD, 240Hz, 1ms, HDMI',
        {
            "samsung",
            "curvo",
            "wqhd",
            "hdmi",
            "27",
            "240hz",
            "1ms",
            "app",
            "odyssey",
            "monitor",
            "gamer",
        },
    ),
    (
        "SSD Hikvision E3000, 512GB, M.2 2280, NVMe, Leitura 3476MB/s e "
        "Gravação 3137MB/s, HS-SSD-E3000/512G",
        {
            "e3000",
            "3476mbs",
            "hikvision",
            "hs",
            "e3000512g",
            "3137mbs",
            "gravação",
            "ssd",
            "2280",
            "nvme",
            "512gb",
            "m2",
            "leitura",
        },
    ),
    (
        "[AME R$ 10,49 / AME SC R$ 7,34 ] - Livro - O milagre da manhã: "
        "O segredo para transformar sua vida",
        {
            "livro",
            "segredo",
            "vida",
            "sc",
            "milagre",
            "sua",
            "1049",
            "manhã",
            "para",
            "ame",
            "734",
            "transformar",
            "da",
        },
    ),
    (
        "Cupom Insider de 20% OFF primeira compra!",
        {"cupom", "20", "off", "primeira", "de", "insider", "compra"},
    ),
    (
        "Comprar o Assassin's Creed® Odyssey - EDIÇÃO ULTIMATE | Xbox",
        {"creed", "ultimate", "xbox", "comprar", "odyssey", "assassins", "edição"},
    ),
    (
        '[AME R$2960]Smart TV 65" Crystal UHD 4K Samsung 65BU8000 (R$ 962,00 cashback pela ame)',
        {
            "cashback",
            "65bu8000",
            "uhd",
            "2960",
            "samsung",
            "65",
            "96200",
            "smart",
            "4k",
            "ame",
            "tv",
            "pela",
            "crystal",
        },
    ),
    (
        "Monitor Gamer Mancer Valak ZX240H, 27Pol., VA, FHD, 1ms, 240Hz, "
        "Freesync e G-Sync, HDMI/DP, MCR-VZX240H-BL01",
        {
            "vzx240h",
            "27pol",
            "monitor",
            "1ms",
            "gamer",
            "mancer",
            "240hz",
            "bl01",
            "freesync",
            "fhd",
            "sync",
            "va",
            "hdmidp",
            "valak",
            "mcr",
            "zx240h",
        },
    ),
    (
        "[AME R$ 107 R$ SC 32 ] Piscina Inflável Fast Set 2.490 Litros - brink+",
        {"ame", "32", "2490", "brink", "set", "piscina", "fast", "inflável", "sc", "107", "litros"},
    ),
    (
        "Need for Speed™ Heat Edição Deluxe[PS4]",
        {"for", "need", "heat", "edição", "deluxe", "speed", "ps4"},
    ),
    (
        "Compre 2 leve 3 Shampoo Anticaspa Head & Shoulders 400ml",
        {"head", "shoulders", "leve", "anticaspa", "compre", "shampoo", "400ml"},
    )
]

TEST_GET_PROMOTION_INFO_PARAMS = [
    (
        {
            "id": "45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
            "title": '[AME R$2960]Smart TV 65" Crystal UHD 4K Samsung 65BU8000 '
            "(R$ 962,00 cashback pela ame)",
            "price": 3699.99,
            "image": {
                "original": "https://api.pelando.com.br/media/f55db4fb-074c-4a31-b102-eaa3a982e88b?v=2"
            },
        },
        {
            "id": "45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
            "title": '[AME R$2960]Smart TV 65" Crystal UHD 4K Samsung 65BU8000 '
            "(R$ 962,00 cashback pela ame)",
            "price": "R$ 3.699,99",
            "url": "https://www.pelando.com.br/d/45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
            "image": "https://api.pelando.com.br/media/f55db4fb-074c-4a31-b102-eaa3a982e88b?v=2",
            "tags": {
                "cashback",
                "65bu8000",
                "uhd",
                "2960",
                "samsung",
                "65",
                "96200",
                "smart",
                "4k",
                "ame",
                "tv",
                "pela",
                "crystal",
            },
        },
    ),
    (
        {
            "id": "215dfe1d-ed62-4a07-b8bf-71176d8b47fc",
            "title": "Jogo Metro Last Light Redux - PC",
            "price": 0,
            "image": {
                "original": "https://api.pelando.com.br/media/ff95c1ec-f330-4457-8221-186c6616c697?v=2"
            },
        },
        {
            "id": "215dfe1d-ed62-4a07-b8bf-71176d8b47fc",
            "title": "Jogo Metro Last Light Redux - PC",
            "price": "Grátis",
            "url": "https://www.pelando.com.br/d/215dfe1d-ed62-4a07-b8bf-71176d8b47fc",
            "image": "https://api.pelando.com.br/media/ff95c1ec-f330-4457-8221-186c6616c697?v=2",
            "tags": {"jogo", "last", "redux", "metro", "pc", "light"},
        },
    ),
]

TEST_CLEAN_DB_DELETE_PROMOTION_INFO_DATA = [
    {
        "id": "45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
        "title": '[AME R$2960]Smart TV 65" Crystal UHD 4K Samsung 65BU8000 '
        "(R$ 962,00 cashback pela ame)",
        "price": "3699.99",
        "url": "https://www.pelando.com.br/d/45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
        "image": "https://api.pelando.com.br/media/f55db4fb-074c-4a31-b102-eaa3a982e88b?v=2",
        "tags": {
            "65",
            "samsung",
            "smart",
            "cashback",
            "pela",
            "tv",
            "ame",
            "4k",
            "96200",
            "65bu8000",
            "2960",
            "crystal",
            "uhd",
        },
    },
    {
        "id": "215dfe1d-ed62-4a07-b8bf-71176d8b47fc",
        "title": "Jogo Metro Last Light Redux - PC",
        "price": "Grátis",
        "url": "https://www.pelando.com.br/d/215dfe1d-ed62-4a07-b8bf-71176d8b47fc",
        "image": "https://api.pelando.com.br/media/ff95c1ec-f330-4457-8221-186c6616c697?v=2",
        "tags": {"jogo", "last", "redux", "metro", "pc", "light"},
    }
]

TEST_WEBHOOK_MOCK_DATA = {
    "update_id": 123456789,
    "message": {
        "message_id": 123,
        "from": {
            "id": 1588357893,
            "is_bot": False,
            "first_name": "Euae™",
            "language_code": "pt-BR"
        },
        "date": 999999999999,
        "chat": {
            "id": 123456789,
            "type": "private",
            "first_name": "Testr",
            "all_members_are_administrators": False
        },
        "forward_from_message_id": 0,
        "text": "/stop",
        "delete_chat_photo": False,
        "group_chat_created": False,
        "supergroup_chat_created": False,
        "channel_chat_created": False,
        "migrate_to_chat_id": None,
        "migrate_from_chat_id": None
    }
}
