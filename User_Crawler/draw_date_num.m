function draw_date_num()
    fid = fopen('./data/cross-site-linking/date_csl_ratio.csv', 'rt');
    C = textscan(fid, '%f %f %f %f %f %s %s %f', 'Delimiter', ',', 'HeaderLines', 1);
    fclose(fid);
    dt = datenum(C{6}, 'yyyymmdd');
    plot(dt, C{5}, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    hold on;
    datetick('x', 'mmm yyyy', 'keeplimits');
    xlim([datenum('08-01-2012') datenum('08-01-2016')]);
    NumTicks = 5;
    L = get(gca,'XLim');
    set(gca,'XTick',linspace(L(1),L(2),NumTicks))
    datetick('x', 'mmm yyyy', 'keeplimits', 'keepticks');
    set(gca, 'FontSize', 12);
    xlabel('','FontSize',20);
    ylabel('Number of Users','FontSize',20);
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/csl/date_num_users.eps', '-depsc');
end
