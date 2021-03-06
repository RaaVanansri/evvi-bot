from logging import exception
import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True, aliases=['j'])
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('You\'re not in a voice channel')
        vc = ctx.author.voice.channel
        if ctx.voice_client is None:
            await vc.connect()
        else:
            await ctx.voice_client.move_to(vc)

    @commands.command(pass_context = True, aliases=['dc'])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(pass_context = True, aliases=['p'])
    async def play(self,ctx, song):
        #ctx.voice_client.stop()
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'}
        YDL_O = {'format':'bestaudio'}
        #vc1 = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_O) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %song, download=False)['entries'][0]
            except Exception:
                return False
        #return{'source':info['formats'][0]['url'], 'title':info['title']}
        url2 = info['formats'][0]['url']
        if ctx.author.voice is None:
            await ctx.send('You\'re not in a voice channel')
        elif ctx.voice_client is None:
            vc = ctx.author.voice.channel
            await vc.connect()
            ctx.voice_client.play(await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS))
            

    @commands.command(pass_context = True, aliases=['pa'])
    async def pause(self, ctx):
        await ctx.voice_client.pause()

    @commands.command(pass_context = True, aliases=['res'])
    async def resume(self, ctx):
        await ctx.voice_client.resume()

def setup(client):
    client.add_cog(music(client))