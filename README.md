# collectd-datacentre

collectd-python plugins useful for monitoring a datacentre.

## onewire_temperature.py

Read the temperatures from an [owfs](http://owfs.org/) directory.

<pre>
&lt;LoadPlugin python&gt;
    Globals true
&lt;/LoadPlugin&gt;

&lt;Plugin python&gt;
    ModulePath &quot;/path/where/module/installed&quot;
    LogTraces true
    Interactive false
    Import &quot;onewire_temperature&quot;

    &lt;Module onewire_temperature&gt;
        OwfsPath "/srv/owfs/uncached"

        # All busses will be read simultaneously, but reading
        # each individual sensor can take ~ 700 milliseconds
        Interval 10
    &lt;/Module&gt;
&lt;/Plugin&gt;
</pre>
