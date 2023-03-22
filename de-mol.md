# How to create automatic subtitles (e.g., for De Mol from Dutch to English)

Preamble:
I'll try to describe here the workflow the best I can to anyone not familiar with software development tools. I'm also on a Windows machine; in principle, the whole workflow can also be done on macOS or Linux. (One caveat for macOS though: You will not be able to use a graphics processor, which makes things go much slower.)

The biggest hurdle to master may be that you need to be able to use yor computer system's command prompt. In Windows, this is `cmd` or, more modern, `powershell`. In macOS, there is a similar prompt/shell program for this. If you are not familiar with using the command line, look for tutorials on the web/youtube.

## In general, what are we doing here and how does this work?

We are going to use an open source AI (Whisper from openAI, https://openai.com/research/whisper) trained to do speech-to-text transformation. I.e., we will not translate any existing subtitles from the video, but instead we'll process the raw audio. The AI is not only capable of writing in text what is said in the video, but also able to translate it to English - e.g., from Dutch to English.

## 1. Install Python

Install Python from here: 

https://www.python.org/downloads/release/python-31010/

At the bottom of the page, you'll find the software packages available; choose the one that fits your system (Windows, macOS).

The latest Python version may not work, thus I link here to Python 3.10, which worked in my case.

## 2. Install pytorch

Though this can be skipped, it is recommeded if you want to be able to use a graphics processor (GPU), which makes the program run much faster. However, currently, the software that is used to run the AI model (pytorch) is *not* supporting fast execution on macOS, so if you are on macOS, this is not for you. Also, you need a graphics processor from NVIDIA to work; AMD's Radeon brand processors are incompatible.

Open your command promopt and type the following commands:

    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117

This may take a while as a lot of stuff has to be downloaded.

## 3. Install the auto_subtitle repository

If not yet open, open your command prompt and type the following command:

    pip install git+https://github.com/orca42/auto-subtitle.git

This will install both the whisper AI and a small tool around it to make working with video files easier.

## 4. Creating subtitles

The AI model comes in several sizes, from `small` over `medium` to `large`. A larger size means a more capable model, doing less errors when understanding speech and, particularly, translating it to a different language at the same time. However, a larger model will also be slower as it requires more compute power, and it will consume more memory.

To not go into too much detail, there are two main options:

Option A: If you have a dedicated graphics card in your computer, this will make things run much faster. You will, however, be limited by the memory of your graphics card; e.g., the `large` AI model requires about 10 GB of graphics memory, which only the latest, expensive cards have. The `medium` model requires about 5 GB, which may be in range.

Option B: If you either have no NVIDIA graphics card (e.g., run this on a laptop) or if you want to use the `large` AI model, you will use only your computer's main processor. This will be *much* slower but is guaranteed to work.

If at some point you encounter program errors, see the last section further below.

### Option A: With graphics card support

In your command prompt, navigate (using `cd`) to the directory where your input video file resides. You need the following command:

    auto_subtitle --task translate --model large -o output\ --language dutch --srt_only True --cpu_only True your-video.mp4 

Replace `your-video.mp4` with whatever filename your video has. 
The subtitle file (.srt) will be created in a new subdirectory `output`. 

What will happen?

The program will start with downloading the `medium` model. This is about 1.4 GB in size and may take a while. On my machine/network, I had really trouble getting this download completed without errors. I had to use an entirely different network. If you run into that, well, go to someone else's network and try again.

Incidentally, others have experienced these problems as well, and the OpenAI developers posted a link somewhere to download the model from an alternative location:

https://openaipublic.blob.core.windows.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt

Alas, I could not find any other link like this, e.g., for the large model.

If you download this manually, you have to put it in a special directory under your home folder: `/your/home/folder/.cache/whisper`.

### Option B: Using the large (best) model, but slower

Same instructions as for option A, but use this as command (in the directory where your video is):

    auto_subtitle --task translate --model large -o output\ --language dutch --srt_only True --cpu_only True your-video.mp4 

Again, replace the last part `your-video.mp4` with your actual video's file name.

Details:
* `cpu_only True` tells it to only use the main processor
* `--model large` will tell it to use the large AI model. Replace this with `--model small` or `--model medium` to use the faster/simpler AI models.

Note:
The large model is about 3 GB in size to download.

## Further remarks

Since I did not write the whole script but slightly modified it from someone else's code, the auto_subtitle script has several additional options. E.g., it could also embed subtitles rather than creating a .srt file, and it could also just create subtiutles in the original language (`--task transcribe`)

# Possible errors

## CUDA out of memory

```
torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 20.00 MiB (GPU 0; 6.00 GiB total capacity; 5.09 GiB already allocated; 0 bytes free; 5.39 GiB reserved in total by PyTorch) If reserved memory is >> allocated memory try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF
```

If you run into this, then your graphics card's memory is too small. Either use "Option B" (CPU only) or reduce the model's size (e.g., from large to medium or small).

## ffmpeg errors

If you encounter some strange error like **"FileNotFoundError: [WinError 2] The system cannot find the file specified"** - and you are pretty sure that you specified the video file correctly - look here:
https://stackoverflow.com/questions/73845566/openai-whisper-filenotfounderror-winerror-2-the-system-cannot-find-the-file

It doesn't look like this at first sight, but this error is related to `ffmpeg`.
The program relies on the ffmpeg software library to extract the audio signal from the video file. I've had to fiddle a lot with this; look at the answers given at the link above, maybe that helps. 
What helped me was to download `ffmpeg` manually (https://ffmpeg.org/download.html) and simply copy the `ffmpeg.exe` program to the same location I run the script from.