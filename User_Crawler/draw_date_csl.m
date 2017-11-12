function draw_date_csl()
    fid = fopen('./data/cross-site-linking/date_csl_ratio.csv', 'rt');
    C = textscan(fid, '%f %f %f %f %f %s', 'Delimiter', ',', 'HeaderLines', 1);
    fclose(fid);
    dt = datenum(C{6}, 'yyyymmdd');
    plot(dt, C{1}.*2, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    hold on;
    plot(dt, C{2}.*2, 'color', 'r', 'LineStyle', '--', 'LineWidth', 2);
    hold on;
    plot(dt, C{3}.*2, 'color', 'g', 'LineStyle', '-.', 'LineWidth', 2);
    hold on;
    plot(dt, C{4}.*2, 'color', 'b', 'LineStyle', ':', 'LineWidth', 2);
    ylim([0 1]);
    datetick('x', 'mmm yyyy', 'keeplimits');
    xlim([datenum('08-20-2012') datenum('08-01-2016')]);
    NumTicks = 5;
    L = get(gca,'XLim');
    set(gca,'XTick',linspace(L(1),L(2),NumTicks))
    datetick('x', 'mmm yyyy', 'keeplimits', 'keepticks');
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    ax = gca;
    ax.XAxis.FontSize = 18;
    xlabel(' ','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    legend('Neither', 'TW only', 'FB only', 'Both', 'Location', 'NorthEast');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/csl/date_csl.eps', '-depsc')
end