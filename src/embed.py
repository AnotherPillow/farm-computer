import discord

def colourFromHex(hex: str) -> tuple:
    return (
        int(hex[1:3], 16),
        int(hex[3:5], 16),
        int(hex[5:7], 16)
    )

def fromDict(dict: dict):
    return EmbedBuilder(
        title=dict['title'] if 'title' in dict else '',
        url=dict['url'] if 'url' in dict else '',
        description=dict['description'] if 'description' in dict else '',
        fields=dict['fields'] if 'fields' in dict else None,
        color=discord.Color.from_rgb(*colourFromHex(dict['str_color']) if 'str_color' in dict else (0, 0, 0)),
        
        str_color=dict['str_color'] if 'str_color' in dict else None,
        footer=dict['footer'] if 'footer' in dict else None,
        thumbnail=dict['thumbnail'] if 'thumbnail' in dict else None,
        image=dict['image'] if 'image' in dict else None,
    )

class EmbedBuilder:

    def __init__(
        self,
        title: str = '',
        url: str = '',
        description: str = '',
        fields: list = None,
        color: discord.Color = discord.Color.default(),
        str_color: str = '#000000',
        footer: str = None,
        thumbnail: str = None,
        image: str = None,
    ):
        self.title = title
        self.url = url
        self.description = description
        self.fields = fields
        self.color = color
        self.str_color = str_color
        self.footer = footer
        self.thumbnail = thumbnail
        self.image = image

    def __str__(self) -> str:
        # return self.build() as a dict
        return str(self.build().to_dict())

    def build(self):
        embed = discord.Embed(
            title=self.title,
            description=self.description,
            color=self.color
        )

        if self.fields:
            for field in self.fields:
                embed.add_field(
                    name=field['name'],
                    value=field['value'],
                    inline=field['inline']
                )
        if self.url:
            embed.url = self.url
        if self.footer:
            embed.set_footer(text=self.footer)

        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)

        if self.image:
            embed.set_image(url=self.image)

        return embed
