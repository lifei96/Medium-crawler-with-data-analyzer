function draw_date_csl()
    fid = fopen('./data/cross-site-linking/date_csl_ratio.csv', 'rt');
    C = textscan(fid, '%f %f %f %f %s', 'Delimiter', ',', 'HeaderLines', 1);
    fclose(fid);
    dt = datenum(C{5}, 'yyyymmdd');
    plot(dt, C{1}, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    hold on;
    plot(dt, C{2}, 'color', 'r', 'LineStyle', '--', 'LineWidth', 2);
    hold on;
    plot(dt, C{3}, 'color', 'g', 'LineStyle', '-.', 'LineWidth', 2);
    hold on;
    plot(dt, C{4}, 'color', 'b', 'LineStyle', ':', 'LineWidth', 2);
    ylim([0 1]);
    datetick('x', 'mmm yyyy', 'keeplimits');
    xlim([datenum('09-01-2012') datenum('08-29-2016')]);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    legend('Neither', 'TW only', 'FB only', 'Both', 'Location', 'NorthEast');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/csl/date_csl.eps', '-depsc')
end