using System;
using System.Globalization;
using System.Windows.Data;
using System.Windows.Media;

namespace SaraServerAgent.Converters
{
    public class StatusToColorConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is not ServerStatus status)
                return new SolidColorBrush(Color.FromRgb(156, 163, 175));

            bool isBg = parameter is string s && s == "bg";

            Color color = status switch
            {
                ServerStatus.Running => Color.FromRgb(74, 222, 128),
                ServerStatus.Starting => Color.FromRgb(251, 191, 36),
                ServerStatus.Restarting => Color.FromRgb(251, 191, 36),
                ServerStatus.Error => Color.FromRgb(248, 113, 113),
                ServerStatus.Stopped => Color.FromRgb(156, 163, 175),
                _ => Color.FromRgb(156, 163, 175)
            };

            return new SolidColorBrush(color);
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            => throw new NotImplementedException();
    }

    public class BoolToOpacityConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            return value is bool b && b ? 1.0 : 0.4;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            => throw new NotImplementedException();
    }
}
