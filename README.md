# curly-carnival

This project simulates and analyzes an autonomous agent performing multi-object navigation tasks on an unexplored building floor plan. Given a list of objects, the primary objective of the autonomous agent is to navigate the building and find an instance of each object. We can model the unexplored floor plan as a two-dimensional grid world. The analysis considers the following components of the system:

 - **Stimulation environment**: This project will provide a two dimensional grid world environ- ment that represents a ”top-down” view of a building’s lay out.
 - **Safety and liveliness monitor**: The system will include a safety and liveliness monitor to ensure the behavior of the navigation system.
 - **Online search policy**: We can model the system as a Markov decision process and use an online search policy like Monte Carlo tree search to find target objects in the environment.


Given these components, I will model this system as a system with synchronous reactive com- ponents. I can define a safety requirement so that the autonomous agent never collides with the walls of the building. Additionally, I will consider liveliness conditions to ensure the agent will keep searching until all objects are found. After exploring the model-based design of this system, I will simulate it with both Python and Julia programs.

Although this idea is not novel, state of the art planning algorithms rely on simulated systems to test their search policy. Furthermore, if novel planning algorithms were to be used in the cyber- physical systems context, a rigorous framework is necessary to assure its behavior. An aspirational goal of this project would be to inject real-world knowledge of the environment into the system by integrating a large-language model into the search policy. Exploring such algorithms for real-world application needs a rigorous framework to ensure safety, reliability and effectiveness.

## Create the environment

```{bash}
conda env create --file environment.yml
```

## To run the simulator:

**CS 6376 Project**

```{bash}
cd curly-carnival
python MultiObjectSearch/do_search.py
```

By default the gridword is set to a 9x9 grid with 10 tokens. The maximum number of steps is 16. The distrbution of tokens is randomized.

These parameters can be altered by modifying lines 23-27 in [do_search.py](MultiObjectSearch/do_search.py)

The map descriptions are all specified in [MAPS.yaml](MultiObjectSearch/MAPS.yaml). You can add additional maps by copying the format of the maps included. After creating a custom map be sure to change the map name vairiable found in line 23 of [do_search.py](MultiObjectSearch/do_search.py).




# LLM Config 

## Llama set up

```
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
MAKE 
```

### Quantize llama model

See https://github.com/facebookresearch/llama-recipes/blob/main/demo_apps/HelloLlamaLocal.ipynb

```
python3 -m pip install -r requirements.txt
python convert.py <path_to_your_downloaded_llama-2-13b_model>
./quantize <path_to_your_downloaded_llama-2-13b_model>/ggml-model-f16.gguf <path_to_your_downloaded_llama-2-13b_model>/ggml-model-q4_0.gguf q4_0
```