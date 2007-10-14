using System;
using System.IO;
using System.Globalization;

using System.Windows;
using System.Windows.Input;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;

namespace CPULoad
{
	public struct CpuCounter {
		long user;
		long nice;
		long system;
		long idle;
		long iowait;
		long irq;
		long softirq;
		long steal;
		long total;
		
		public void Read (String line) {
			String[] parts = line.Split (new char[] {' '}, StringSplitOptions.RemoveEmptyEntries);
			total += (user = long.Parse (parts [1]));
			total += (nice = long.Parse (parts [2]));
			total += (system = long.Parse (parts [3]));
			total += (idle = long.Parse (parts [4]));
			total += (iowait = long.Parse (parts [5]));
			total += (irq = long.Parse (parts [6]));
			total += (softirq = long.Parse (parts [7]));
			total += (steal = long.Parse (parts [8]));
		}

		public CpuCounter Sub (ref CpuCounter other) {
			CpuCounter res = this;
			res.user -= other.user;
			res.nice -= other.nice;
			res.system -= other.system;
			res.idle -= other.idle;
			res.iowait -= other.iowait;
			res.irq -= other.irq;
			res.softirq -= other.softirq;
			res.steal -= other.steal;
			res.total -= other.total;
			return res;
		}

		public void FetchGlobalCounters() {
			using ( StreamReader sr = new StreamReader ("/proc/stat")) {
				String line = sr.ReadLine ();
				Read (line);
			}
		}
		
		public double CpuLoad () {
			return 100d * ((double)(total - idle) / total);
		}
	}

	public class CpuMonitorPanel : Canvas 
	{
		Shape cpurect;
		TextBlock load;
		CpuCounter last;
		ColorAnimation colorAnim;
		Storyboard colorSb;

		public void DrawLoad ()
		{
			CpuCounter cur = new CpuCounter ();
			cur.FetchGlobalCounters ();
			CpuCounter delta = cur.Sub (ref last);
			last = cur;
    		
			double num = Math.Round (delta.CpuLoad ());
			load.Text = ((int)num).ToString ();
			Color current = (cpurect.Fill as SolidColorBrush).Color;
			Color color = new Color ();

			if (num <= 50) {
				//interpolate (0,50) between green (0,255,0) and yellow (255,255,0)
				double red = num / (50d / 255);
				color = Color.FromRgb ((byte)red, 255, 0);
			} else {
				//interpolate (50,100) between yellow (255,255,0) and red (255,0,0)
				double green = (100d - num) / (50d / 255);
				color = Color.FromRgb (255, (byte)green, 0);
			}

			colorAnim.From = current;
			colorAnim.To = color;
			colorSb.Begin ();
		}

		public void PageLoaded (object o, EventArgs e) 
		{
			cpurect = FindName ("CPULoadRectangle") as Shape;
			load = FindName ("Load") as TextBlock;
			colorSb = FindName ("color_sb") as Storyboard;
			colorAnim = FindName ("color_anim") as  ColorAnimation;
			last = new CpuCounter ();

			Storyboard sb = FindName ("run") as Storyboard;
			DoubleAnimation timer = new DoubleAnimation ();
			((TimelineCollection)sb.GetValue(TimelineGroup.ChildrenProperty)).Add(timer);
			timer.Duration = new Duration (TimeSpan.FromMilliseconds (100));

			sb.Completed += delegate {
				DrawLoad ();
				sb.Begin ();
			};
			sb.Begin ();
			DrawLoad ();
		}
	}
}
