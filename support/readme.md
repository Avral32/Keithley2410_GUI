======================= Status of Project ============================
The whole program works properly both voltage and time scanning measurements unless 
you concern much about speed and neatness.

There are a few problems needed to be optimized. The live plot is not optimized 
by the time when it was finished. So the live plots are implemented with Drawnow package,
which draws the plot outside of *tkinter* object. Even worse, the reaaction of the script 
gets slower due to a for loop that is used for voltage scan. This is most likely due to 
the fact that the internal loop of the *tkinter* conflickts with the for loop. This drawback
can easily be resolved by implementing the for loop using the built-in `self.after(ms, func, *arg)`
of the tkinter, as demontrated in **liveplot_classobj.py** molude in the subfolder.

In addtion, the logic of the created class object (**Keith2140**) needs to be improved by 
using the basic properties of the class. For example, using the `@staticmethod` to omit some 
unnecessary arguments in some methods. by adding `@property` to a method, we could make an instance
from that method without any arguments just like an atribute. Therefore, there is a room to 
work on to improve the current project. The mostly used basic properties of the class is 
summarized in three markdown files in the subfolder **object oriented program**.  